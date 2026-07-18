#!/usr/bin/env python3
"""Update public live source status data for Mob Deals.

This script deliberately records source reachability and public price-token signals,
but it does not automatically publish provider prices as verified deals. Provider
prices require human review because checkout prices, promotions and terms change.
"""
from __future__ import annotations

import json
import re
import ssl
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
PROVIDERS_PATH = ROOT / "data" / "providers.json"
OUT_PATH = ROOT / "data" / "live-sources.json"

GBP_RE = re.compile(r"£\s?\d+(?:\.\d{2})?")


def fetch(url: str) -> dict:
    req = Request(
        url,
        headers={
            "User-Agent": "MobDealsSourceCheck/1.0 (+https://dlinacre.github.io/mob-deals/)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    context = ssl.create_default_context()
    try:
        with urlopen(req, timeout=20, context=context) as response:
            body = response.read(250_000)
            text = body.decode("utf-8", errors="ignore")
            tokens = sorted(set(GBP_RE.findall(text)))[:12]
            return {
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
    results = []
    for provider in providers:
        result = fetch(provider["sourceUrl"])
        results.append({
            "id": provider["id"],
            "provider": provider["name"],
            "network": provider.get("network", ""),
            "sourceUrl": provider["sourceUrl"],
            **result,
        })

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
