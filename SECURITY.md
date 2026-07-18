# Security Policy

Mob Deals is a static GitHub Pages website. Security reports should be defensive and limited to publicly accessible website/repository concerns.

## Supported surface

- Live site: https://dlinacre.github.io/mob-deals/
- Repository: https://github.com/DLinacre/mob-deals

## Reporting a vulnerability

Please open a private security advisory if available, or open a GitHub issue with enough detail to reproduce the issue safely. Do not include exploit payloads that target third parties or private systems.

## Scope

In scope:

- Exposed secrets committed to this repository
- Broken access-control assumptions in the public static site
- Unsafe third-party script usage
- Defensive header/privacy recommendations
- Accessibility/security overlap such as deceptive links or unsafe external navigation

Out of scope:

- Denial-of-service testing
- Social engineering
- Attacks against GitHub, providers, Ofcom, or any third-party website
- Attempts to bypass provider controls or scrape private/authenticated data

## Current security posture

- Static files only
- No login or account system
- No analytics, cookies, payments, or contact forms at launch
- External links use `rel="noopener noreferrer"`
- Meta CSP/referrer policy included for defence in depth; full HTTP security headers require a hosting/CDN layer that supports custom headers
