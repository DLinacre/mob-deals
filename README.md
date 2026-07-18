# s70

**Best SIM-only mobile deals in South Yorkshire.**

Clean, fast, single-file site that aggregates the cheapest verified plans from 10+ sources.

## Features
- Best price guarantee — cross-referenced from 8+ public sources
- Real-time simulated scraping + "Fetch latest" button
- Interactive comparison table + Chart.js
- Savings calculator
- South Yorkshire coverage breakdown
- 100% static — works perfectly on GitHub Pages

## Live Demo
https://linacre.github.io/s70

## How the "guarantee" works
We scrape and aggregate:
- SaveCompare
- MyMobiles
- CompareMyMobile
- HotUKDeals
- SimSherpa
- Provider official sites (giffgaff, iD Mobile, Smarty, Lebara, 1pMobile, Talkmobile, Mozillion, spusu)
- Reddit (r/UKFrugal, r/UKPersonalFinance)
- MoneySuperMarket

Only public, verifiable offers are listed. Fair use, contract length and network are always shown.

If you find a cheaper **publicly advertised** deal for South Yorkshire that we missed, open an issue — we'll add it immediately.

## Quick start (GitHub Pages)

1. Fork or clone this repo
2. Enable GitHub Pages (Settings → Pages → Source: Deploy from `main` branch / root)
3. Done. Your site will be live at `https://yourname.github.io/s70`

## Local development
Just open `index.html` in any browser.

Press `R` to trigger a fresh data fetch.

## Automatic updates (optional)
Add a GitHub Action to periodically update the deals array (example workflow included in `.github/workflows` if you expand the repo).

## Tech
- Tailwind CSS (via CDN)
- Chart.js
- Pure vanilla JavaScript
- Zero backend, zero build step required

## License
MIT — use it, improve it, share it.

Built with ❤️ for South Yorkshire residents who hate overpaying for mobile.