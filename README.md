# AnyUnit - Unit Converter Project Requirements

## 1. Project Overview

### 1.1 Purpose

Create a high-performance, SEO-friendly unit converter web application that allows users to convert between different units of measurement and apparel sizes. The application will use static files instead of a database for better performance and easier deployment. It is extendible to keep adding different services for calculators,
converters, and different tools to convert files, download files, interact with web services. In the future the 
application will be expanded to add multiple other useful services, therefore it should be easily extendible.

### 1.2 Tech Stack

* **Backend**: Flask (Python 3.13)
* **Frontend**: HTML5, CSS3, JavaScript (ES6+)
* **CSS Framework**: Bootstrap 5

## 2. Project Structure

```plaintext
anyunit/
├── app/
│   ├── static/
│   │   ├── js/
│   │   │   ├── services/           # Unit-specific conversion logic, and different services in the future
│   │   │   ├── components/          # Reusable UI components
│   │   │   └── utils/               # Helper functions
│   │   ├── css/
│   │   ├── data/                    # Static data files
│   │   └── img/
│   ├── templates/
│   │   ├── base.html
│   │   ├── components/              # Reusable template components
│   │   ├── pages/                   # Dynamic pages
│   │   └── static_pages/            # Pre-generated conversion pages
│   ├── utils/                       # Python utility functions
│   └── routes/                      # Flask route handlers
├── config/                          # Configuration files
└── scripts/                         # Build and maintenance scripts
```

## 3. Data Structure

### 3.1 Units Data (`static/data/units.json`)

```json
{
  "categories": {
    "length": {
      "title": "Length",
      "description": "Convert between length units",
      "icon": "📏",
      "units": {
        "m": {
          "name": "Meter",
          "symbol": "m",
          "factor": 1,
          "type": "SI",
          "popular": true
        }
      },
      "popular_conversions": [
        {"from": "m", "to": "ft"},
        {"from": "km", "to": "mi"}
      ]
    }
  }
}
```

### 3.2 Conversion Tables

Pre-generated tables for common conversions are stored in `static/data/tables/` to improve SEO and user experience.

## 4. Feature Requirements

### 4.1 Core Features

* Unit conversion with real-time calculation
* Support for multiple unit categories (length, weight, temperature, etc.)
* Conversion history (localStorage)
* Copy results to clipboard
* Share conversion links
* Mobile-responsive design
* Conversion for apparel sizes
* Static tables with conversions
* Printable tables with unit conversions

### 4.2 User Interface

* Clean, intuitive main page with category grid
* Search functionality for units and conversions
* Quick access to popular conversions
* Clear conversion forms with instant results
* Common conversions table on each page
* Mobile-first, responsive design
* Export for printing

### 4.3 Technical Features

* Client-side conversion calculations
* Static page generation for SEO
* URL structure: `/convert/{category}/{from-unit}-to-{to-unit}`
* Caching of static assets
* Error handling and input validation
* Cross-browser compatibility
* High-performance

## 5. Page Types

### 5.1 Main Page

* Category grid with icons
* Popular conversions for each category
* Global search bar
* Quick navigation

### 5.2 Category Pages

* List of all possible conversions within category
* Popular conversions highlighted
* Common conversion tables
* Related categories

### 5.3 Conversion Pages

* Main conversion form
* Common values table
* Formula explanation
* Related conversions
* Meta information for SEO

## 6. Technical Requirements

### 6.1 Performance

* Page load time < 2s
* First contentful paint < 1s
* Time to interactive < 3s
* Cache static assets
* Minimize JavaScript bundle size

### 6.2 SEO

* Server-side rendered content
* Semantic HTML structure
* Meta tags for all pages
* Structured data (JSON-LD)
* Sitemap generation
* Static pages for common conversions

### 6.3 Accessibility

* WCAG 2.1 AA compliance
* Keyboard navigation
* Screen reader support
* Proper ARIA labels
* Color contrast requirements

### 6.4 Browser Support

* Chrome (latest 2 versions)
* Firefox (latest 2 versions)
* Safari (latest 2 versions)
* Edge (latest 2 versions)
* Mobile browsers

## 7. Development Process

### 7.1 Setup

1. Initialize Flask project
2. Set up static file structure

### 7.2 Implementation Phases

1. Core framework and structure
2. Basic conversion functionality
3. UI components and styling
4. Advanced features and optimizations
5. SEO implementation

## 8. Deployment Requirements

### 8.1 Environment

* Python 3.13+
* Heroku hosting

### 8.2 Configuration

* Environment-based settings
* Logging configuration
* Error tracking
* Analytics integration

## 9. Future development

### 9.1 New services

* Industry specific converters and calculators (example: aviation)
* Social media tools (example: download YouTube video/audio)
* Tools to scan websites to download informaiton
* Form fillers

## 10. Future Considerations

### 10.1 Potential Features

* API access
* User accounts
* Custom unit definitions
* Mobile app version
* Offline support (PWA)

### 10.2 Scalability

* CDN integration
* Static asset optimization
* Caching strategies
* Performance optimization

---

## Current Application Overview

AnyUnit is an SEO-friendly Flask web application for unit and apparel size conversion with additional utilities and calculators.

- Backend: Flask 3.1 (Python 3.13), Blueprints architecture
- Frontend: HTML, Bootstrap 5, vanilla JS
- Data: Static JSON in `app/static/data/` (no DB)
- Hosting: Compatible with Heroku via `Procfile`

### Key Features Implemented

- Unit conversion with real-time calculations via `/api/convert`
- Category and conversion pages with common values tables
- Quick Converter UI on conversion pages powered by `app/static/js/quick-converter.js`
- Aviation calculators (Blueprint `app/routes/aviation.py`):
  - Fuel requirements (distance, IAS, wind, reserve)
  - Ground speed (IAS→TAS approximation, wind components, density altitude)
  - Density altitude (rule-of-thumb formula)
- Markdown to DOCX/HTML utilities (`app/routes/markdown_converter.py`)
- Timezone and text file tools (`app/routes/timezone.py`, `app/routes/text_files.py`)
- SEO helpers (`app/utils/seo.py`) for meta tags

### Project Structure (selected)

- `app/__init__.py` — app factory and blueprint registration
- `app/routes/` — view routes for main pages, converter, APIs, aviation, etc.
- `app/utils/` — core logic: `unit_converter.py`, `aviation_calculations.py`, `seo.py`
- `app/templates/` — Jinja templates for pages and components
- `app/static/` — CSS/JS assets and data JSON files

### Running Locally

1) Python 3.13

2) Install dependencies

```bash
pip install -r requirements.txt
```

3) Set environment variables (development defaults are supported)

```bash
export SECRET_KEY="change-me"
export DEBUG=true
```

4) Start the server

```bash
python run.py
# or
gunicorn run:app
```

### Core APIs

- POST `/api/convert`
  - JSON: `{ "category": str, "fromUnit": str, "toUnit": str, "value": number }`
  - Returns: `{ success, result, formatted }`

- POST `/aviation/api/aviation/fuel-calc`
  - JSON: `{ distance, indicatedAirspeed, fuelConsumption, windSpeed, windDirection, heading, reserveTime }`
  - Returns: `{ ground_speed, flight_time (min), fuel_required, reserve_fuel }`

- POST `/aviation/api/aviation/ground-speed`
  - JSON: `{ indicatedAirspeed, windSpeed, windDirection, heading, temperature, pressureAltitude }`
  - Returns: `{ ground_speed, density_altitude, headwind_component, crosswind_component }`

- POST `/aviation/api/aviation/density-altitude`
  - JSON: `{ pressureAltitude, temperature }`
  - Returns: `{ density_altitude }`

### Notes on Calculations

- Unit conversions use base-factor ratios in `app/static/data/units.json`; temperatures use explicit formulas in `app/utils/unit_converter.py`.
- Aviation ground speed uses TAS minus headwind component with TAS ≈ IAS × (1 + 0.02 × PA/1000).
- Density altitude uses a standard rule-of-thumb: DA = PA + 120 × (OAT − ISA Temp).


## Proposed Improvements

### UX Enhancements

- Form validation and hints
  - Add `min`, `max`, and `step` attributes consistently and inline help text (e.g., “Wind direction is FROM direction”).
- Accessibility and keyboard flow
  - Ensure labels/aria attributes and focus states meet WCAG 2.1 AA; verify tab order.
- Better error handling
  - Inline field-level errors and non-blocking alerts; avoid general error banners when a single field is invalid.
- Persisted user preferences
  - Remember last-used category/units and recent values with `localStorage`.
- Results clarity
  - Show formulas used and intermediate components (e.g., headwind/crosswind) with tooltips.
- Mobile polish
  - Larger touch targets and improved responsive spacing for calculators.

### SEO Improvements

- Rich metadata per page
  - Generate canonical URLs, meta descriptions, and Open Graph/Twitter tags dynamically via `seo.py`.
- Structured data (JSON-LD)
  - Add `BreadcrumbList` and `SoftwareApplication` (or `WebSite`) schema on key pages.
- Sitemap and robots
  - Provide `/sitemap.xml` for popular conversions and allow crawl via `robots.txt`.
- Static page pre-rendering
  - Pre-generate static HTML for top conversion pairs for crawl speed and long-tail queries.
- Internal linking
  - Expand related conversions and category cross-links to improve crawl paths.

### Engagement Features

- Favorites and history UI
  - Promote the existing history to a visible panel; allow starring favorite conversions.
- Share and embed
  - One-click share with prefilled conversion URLs; copy snippet to embed tables.
- PWA support
  - Installable app with offline cache for common conversions and calculators.
- Educational content
  - Add brief explanations and examples for each category and aviation calculator.

### Performance

- HTTP caching and compression
  - Far-future cache for static assets, gzip/brotli on responses.
- Asset optimization
  - Minify and bundle CSS/JS, defer non-critical scripts, preload critical CSS.
- CDN and image optimization
  - Host static assets on a CDN; provide responsive icons and proper `sizes`.

### Developer Experience

- Tests
  - Add unit tests for conversion math and aviation calculators.
- Observability
  - Structured logging of API errors and basic analytics events.


## Recent Fixes (Summary)

- Proper boolean handling for `DEBUG` and default `SECRET_KEY` in `config.py`.
- Aviation math corrections in `app/utils/aviation_calculations.py`:
  - Ground speed from TAS minus headwind component; TAS approximation from IAS and pressure altitude.
  - Removed incorrect ground speed scaling by density altitude.
- Unique IDs per aviation form in `app/templates/aviation/index.html` and updated JS selectors to prevent cross-form interference.

## SEO Implementation

The application includes a set of SEO features to improve crawlability, SERP appearance, and sharing previews.

### Implemented

- Canonical URLs
  - Rendered in `app/templates/base.html` using `meta_tags.canonical` or current URL fallback.
- Open Graph and Twitter Cards
  - OG and Twitter meta tags added in `base.html` for title, description, URL, site_name, and image.
  - Twitter card uses `summary_large_image` by default.
- JSON-LD Structured Data
  - `app/utils/seo.py` now returns `json_ld` when `base_url` is provided.
  - Homepage: `WebSite` schema.
  - Category and Conversion pages: `BreadcrumbList` schema with 2–3 levels.
- Centralized SEO helper
  - `generate_meta_tags()` enhanced to accept `base_url`, optional overrides, and produce `title`, `description`, `canonical`, and `json_ld`.
  - Used across routes: `main.index`, `converter.convert`, `converter.category`, `aviation.aviation_calculators`, `markdown.index`, `timezone.index`, `text_files.index`, and `privacy_policy`.
- Sitemap and robots
  - `/sitemap.xml` includes home, categories, popular conversions, and utility pages (`markdown`, `timezone`, `text_files`), and aviation landing.
  - `/robots.txt` references the sitemap and disallows `/static/`.
- Error pages
  - `404.html` and `500.html` set `noindex,nofollow` via a `robots` block override in `base.html`.
- Meta blocks fixed
  - `templates/pages/index.html` now uses `{% block meta_description %}` to correctly populate the meta description.

### Files Touched

- `app/utils/seo.py`
  - Added JSON-LD helpers and `base_url` support; accepts manual overrides.
- `app/templates/base.html`
  - Canonical, OG/Twitter tags, JSON-LD rendering, robots block.
- `app/routes/main.py`
  - Pass `base_url`; add `/robots.txt` and `/sitemap.xml`; SEO meta for privacy policy.
- `app/routes/converter.py`
  - Pass `base_url` to `generate_meta_tags()`.
- `app/routes/aviation.py`, `app/routes/markdown_converter.py`, `app/routes/timezone.py`, `app/routes/text_files.py`
  - Inject `meta_tags` into their templates.
- `app/templates/pages/index.html`
  - Fixed meta description block.
- `app/templates/errors/404.html`, `app/templates/errors/500.html`
  - Set `noindex,nofollow`.

### Next SEO Enhancements (Roadmap)

- Social Images
  - Generate per-category/per-conversion OG images for richer link previews (e.g., via an image endpoint or pre-rendered assets).
- Structured Data Expansion
  - Consider `ItemList` or `Dataset` schema for conversion tables on category pages.
- Sitemap Scaling
  - Add pagination and lastmod fields if the URL set grows large. Include more conversion pairs based on analytics.
- i18n / hreflang
  - If adding localized content, generate `hreflang` tags and localized sitemap entries.
- Analytics Events
  - Track conversion and share events for better insight into user behavior (already has GA base).
- Performance and Indexability
  - Preload critical CSS; defer non-critical JS; ensure CLS/INP are optimized for better CWV.
- Meta Copy Refinement
  - Fine-tune titles/descriptions per category/conversion from `units.json` (e.g., add symbols and synonyms) to improve CTR.
