# MOSETY REPOSITORY BASELINE SNAPSHOT (AG001)

**Execution Date**: 28 September 2026  
**Auditor**: Antigravity Autonomous Coding Agent  
**Environment**: Windows 11 / PythonAnywhere Production  
**Primary Domain**: `https://www.mosetyboatridesnaivasha.co.ke/`  
**Git Branch**: `main` (commit `bec9056`)

---

## 1. Runtime & Stack Specifications

| Component | Version / Setting | Notes |
| :--- | :--- | :--- |
| **Python** | 3.12.3 (64-bit) | Local venv & remote WSGI virtualenv |
| **Django** | 6.0.1 | Modern async/sync support, custom sitemaps |
| **Frontend UI** | HTML5, HTMX 1.9.10, Alpine.js 3.x, Tailwind CSS | Progressive enhancement, server-rendered |
| **Database** | SQLite 3 (`db.sqlite3`) | 43 models across 16 custom business apps |
| **Web Server** | WSGI / Nginx (PythonAnywhere) | Workers: `www.mosetyboatridesnaivasha.co.ke` |
| **Production Host** | `mosety.pythonanywhere.com` | SSL valid for `www.mosetyboatridesnaivasha.co.ke` |

---

## 2. Installed Applications (26 total)

- **Django Standard**: `django.contrib.admin`, `auth`, `contenttypes`, `sessions`, `messages`, `staticfiles`, `sitemaps`, `humanize`
- **Third-Party Libraries**: `taggit`, `tinymce`
- **Mosety Business Core Apps**:
  1. `core`: `SiteSettings` singleton, core business data, business identity
  2. `analytics`: UTM capture, event tracking middleware
  3. `tours`: Tour catalog, pricing models, intent tags, duration
  4. `content`: Pillars, Captains, Guides, destination articles
  5. `pages`: Static pages, Home, Contact, Sitemap, Legal (Privacy/Terms), Robots, LLMs
  6. `bookings`: Booking leads, booking calculator, checkout flow
  7. `dashboard`: Staff operational dashboard
  8. `seo`: Local pages, FAQs, redirects, sitemaps, schema utilities
  9. `blog`: Field journal, articles, tagging, SEO bylines
  10. `jobs`: Career listings and guides
  11. `services`: Additional lake activities
  12. `testimonials`: Passenger reviews and testimonials
  13. `accommodation`: Partner hotel listings
  14. `reputation`: Crew profiles, star ratings, leaderboards
  15. `loyalty`: Customer return programs
  16. `resources`: Curated visitor resources, guides, static sitemaps

---

## 3. URL Architecture & Routing

- **Root Routing** (`boats/urls.py`):
  - `/` &rarr; `pages.urls` (Home, Legal, Robots, LLMs, HTML Sitemap)
  - `/boat-rides/` &rarr; `tours.urls` (Tours hub, tour detail, prices)
  - `/crescent-island/`, `/captains/`, `/safety/`, `/reviews/` &rarr; `content.urls`
  - `/bookings/`, `/book/` &rarr; `bookings.urls`
  - `/blog/` &rarr; `blog.urls` (Field journal)
  - `/sitemap.xml` &rarr; Custom `sitemap_clean_view` (No X-Robots-Tag, 1,747 URLs)
  - `/robots.txt` &rarr; Dynamic robots policy with canonical sitemap URL

---

## 4. Current Test Suite Baseline

- Total Tests: **39 passing** (100% success rate).
- Test execution time: ~7.2 seconds.
- Test coverage covers: UTM capture, sitemap dynamic routing, SEO redirects, brand forbidden token assertions, WhatsApp URL generation, canonical URL cleanup.

---

## 5. Preliminary Brand Decontamination Audit Findings

A baseline grep of tracked files and database tables reveals leftover legacy brand tokens:
- **Files with legacy references**:
  - `templates/blog/post_detail.html`: Legacy meta title, publisher schema, logo reference.
  - `templates/bookings/tour_detail.html`: Legacy related tours heading, organization schema.
  - `templates/bookings/tour_list.html`: Legacy meta title.
  - `templates/seo/detail.html`: Legacy publisher name and logo URL.
  - `templates/reputation/` & `templates/testimonials/`: Legacy brand mentions in titles and seed scripts.
  - `utils.py`: Legacy brand comments.
- **Database records with legacy references**:
  - ~1,500 records across `FAQ`, `FAQItem`, `LocalPage`, `Post`, `Tour`, `Testimonial`, and `GuidePage`.
  - User ID 7 (`paradise-editor`).

All these items are queued for systematic neutralization in Phase 0.
