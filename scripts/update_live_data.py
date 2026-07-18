#!/usr/bin/env python3
"""Update public live source status data for Mob Deals.

The script records reachability and public price-token signals from source pages.
It does not automatically verify or publish checkout prices. Provider prices need
human review because promotions, eligibility and basket terms change frequently.
"""
from __future__ import annotations

import json
import re
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS_PATH = ROOT / "data" / "providers.json"
OUT_PATH = ROOT / "data" / "live-sources.json"

GBP_RE = re.compile(r"£\s?\d+(?:\.\d{2})?")
TIMEOUT_SECONDS = 12
MAX_WORKERS = 10


def fetch(provider: dict) -> dict:
    url = provider["sourceUrl"]
    req = Request(
        url,
        headers={
            "User-Agent": "MobDealsSourceCheck/1.0 (+https://dlinacre.github.io/mob-deals/)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    context = ssl.create_default_context()
    base = {
        "id": provider["id"],
        "provider": provider["name"],
        "network": provider.get("network", ""),
        "category": provider.get("category", ""),
        "sourceUrl": url,
    }
    try:
        with urlopen(req, timeout=TIMEOUT_SECONDS, context=context) as response:
            body = response.read(180_000)
            text = body.decode("utf-8", errors="ignore")
            tokens = sorted(set(GBP_RE.findall(text)))[:16]
            return {
                **base,
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "finalUrl": response.geturl(),
                "contentType": response.headers.get("content-type", ""),
                "bytesSampled": len(body),
                "observedPriceTokens": tokens,
                "error": None,
            }
    except HTTPError as exc:
        return {
            **base,
            "status": exc.code,
            "ok": False,
            "finalUrl": getattr(exc, "url", url),
            "contentType": exc.headers.get("content-type", "") if exc.headers else "",
            "bytesSampled": 0,
            "observedPriceTokens": [],
            "error": f"HTTP {exc.code}",
        }
    except (URLError, TimeoutError, ssl.SSLError, OSError) as exc:
        return {
            **base,
            "status": None,
            "ok": False,
            "finalUrl": url,
            "contentType": "",
            "bytesSampled": 0,
            "observedPriceTokens": [],
            "error": exc.__class__.__name__,
        }


def main() -> None:
    providers = json.loads(PROVIDERS_PATH.read_text(encoding="utf-8"))["providers"]
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results_by_id: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(fetch, provider): provider for provider in providers}
        for future in as_completed(futures):
            result = future.result()
            results_by_id[result["id"]] = result

    results = [results_by_id[p["id"]] for p in providers]
    payload = {
        "generatedAt": checked_at,
        "status": "public-source-reachability-check",
        "disclaimer": "Automated source checks show whether public provider pages were reachable and expose raw price-like tokens. They do not verify final checkout prices. Human review is required before publishing deal prices.",
        "sourceCount": len(results),
        "reachableCount": sum(1 for r in results if r["ok"]),
        "sources": results,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
