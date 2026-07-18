<p align="center"><img src="assets/banner.svg" alt="Mob Deals — South Yorkshire SIM-only comparison" width="100%"></p>

# Mob Deals

**Transparent, accessible SIM-only mobile comparison for South Yorkshire.**

Mob Deals is a polished GitHub Pages website built to replace unsupported guarantee claims with clear methodology, provider confirmation links, accessible UI, SEO-ready metadata and fast static delivery.

## Tags

`github-pages` · `static-site` · `mobile-deals` · `sim-only` · `south-yorkshire` · `accessibility` · `seo` · `performance` · `wcag` · `vanilla-js`

## Live site

https://dlinacre.github.io/mob-deals/

## What changed

- Removed fake/random “fresh data” scraping.
- Removed unsupported “lowest price guaranteed” claims.
- Added transparent disclaimers and methodology.
- Added semantic HTML, skip link, accessible labels and visible focus states.
- Added static deal cards/table so content works without JavaScript.
- Added Privacy, Terms, About, Contact, Methodology and Accessibility pages.
- Added sitemap, robots file, manifest, canonical, Open Graph/Twitter metadata and JSON-LD.
- Replaced Tailwind CDN and Chart.js with a small self-hosted CSS/JS footprint.
- Added clean branding assets: banner and icon.

## Repository about

A responsible, SEO-ready and accessibility-first comparison site for South Yorkshire SIM-only mobile deals, deployed on GitHub Pages.

## Project structure

```text
.
├── index.html
├── about.html
├── methodology.html
├── contact.html
├── privacy.html
├── terms.html
├── accessibility.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── manifest.webmanifest
├── .nojekyll
└── assets/
    ├── app.js
    ├── styles.css
    ├── icon.svg
    ├── og.svg
    └── banner.svg
```

## Local development

Open `index.html` directly in a browser, or run a local static server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.

## Deployment

GitHub Pages can deploy directly from the `main` branch root.

## Data policy

The current site uses manually maintained comparison data and provider links. It does **not** claim real-time scraping, guaranteed lowest pricing or live availability. Any future automated pipeline should store source URLs, timestamps, validation results and human approvals before publishing.

## License

MIT, unless changed by the repository owner.
