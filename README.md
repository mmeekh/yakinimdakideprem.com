# Yakınımdaki Deprem

A free, real-time earthquake tracker for Turkey — no ads, no sign-up, no paywall.

Live at **[yakinimdakideprem.com](https://yakinimdakideprem.com)**.

## What it does

Yakınımdaki Deprem aggregates seismic data from official Turkish sources (Kandilli Observatory, AFAD) and presents it as a fast, mobile-friendly map and feed. It is built to be useful in the seconds and minutes after an earthquake, when people need clear information and not a marketing funnel.

Core capabilities:

- Live earthquake list and interactive map for Turkey
- Magnitude filters, recent quakes, and basic statistics
- Province-level pages and earthquake safety guides
- Building risk awareness content and "what to do before/during/after" guides
- Optional X (Twitter) bot that posts a map snapshot, magnitude, and location for each significant event

## Who it's for

- **Residents of Turkey** who want a quick, ad-free way to check what just happened.
- **Journalists and researchers** who need a clean public view of recent seismic activity.
- **Anyone abroad** with family or friends in the region who want a fast, no-login status check.

The site is intentionally simple. If your phone just shook and you want to know what hit, you should land on the answer in one click.

## Tech stack

- **Frontend:** HTML, CSS, vanilla JavaScript — served as static files for speed and resilience.
- **Backend:** FastAPI (Python) for the data API, Twitter bot, and map snapshot generation.
- **Infrastructure:** Caddy as reverse proxy and static server, Docker Compose for deployment.

The frontend is plain HTML/JS on purpose — no SPA, no build step, no client-side framework tax. Pages render fast on a slow phone connection, which is when this site matters most.

## Project layout

```
app/        FastAPI backend (data API, twitter bot)
public/     Static frontend served by Caddy
Caddyfile / Caddyfile.production    Reverse proxy + static config
docker-compose.yml                  Local development
docker-compose.production.yml       Production deployment
scripts/    Maintenance scripts (sitemap, etc.)
```

## Running locally

```bash
docker compose up -d --build
```

Then open `http://localhost` for the site and `http://localhost/docs` for the API.

## Production

```bash
docker compose -f docker-compose.production.yml up -d --build
```

## Motivation

This is a free public service.

There are plenty of earthquake apps and sites in Turkey, but most of them either bury the data under ads, demand sign-ups, push notifications you didn't ask for, or wrap basic public data in a paid subscription. Earthquake information in a country that sits on active fault lines should not be a growth-hacked product.

Yakınımdaki Deprem is built and run by one person, on a personal budget, as a small contribution. The data comes from public sources. The code runs on plain infrastructure. There is no tracking funnel, no premium tier, and no plan to add one.

If the site is useful to you in a hard moment, that's the whole point.
