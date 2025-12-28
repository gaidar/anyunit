# AnyUnit

A high-performance, SEO-friendly unit converter web application built with Flask. Convert between units of measurement, use aviation calculators, transform text files, and more.

## Features

### Unit Conversion
Real-time conversion between units across 8 categories:
- **Length** — meter, kilometer, centimeter, millimeter, inch, foot, yard, mile
- **Weight** — kilogram, gram, milligram, pound, ounce
- **Temperature** — Celsius, Fahrenheit, Kelvin
- **Volume** — liter, milliliter, gallon, quart, pint, cup, fluid ounce
- **Speed** — m/s, km/h, mph, knots
- **Pressure** — Pascal, bar, psi, atm
- **Energy** — joule, calorie, kWh, BTU
- **Power** — watt, kilowatt, horsepower

### Aviation Calculators
- **Fuel Requirements** — calculate fuel needed based on distance, airspeed, wind, and reserve time
- **Ground Speed** — compute ground speed from IAS, wind components, and density altitude
- **Density Altitude** — determine density altitude from pressure altitude and temperature

### Additional Tools
- **Markdown Converter** — convert Markdown to HTML or DOCX
- **Timezone Converter** — convert times between world timezones
- **Text File Converter** — transform between JSON, XML, and CSV formats

## Tech Stack

- **Backend:** Flask 3.1 (Python 3.13)
- **Frontend:** HTML5, Bootstrap 5, vanilla JavaScript (ES6+)
- **Data:** Static JSON files (no database)
- **Server:** Gunicorn (Heroku-ready via Procfile)

## Installation

### Prerequisites
- Python 3.13+
- pip

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd anyunit

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me` | Flask secret key for sessions |
| `DEBUG` | `false` | Enable debug mode (`true`, `1`, `yes`, `on`) |

```bash
export SECRET_KEY="your-secret-key"
export DEBUG=true
```

## Running the Application

### Development
```bash
python run.py
```
Server runs at `http://127.0.0.1:5000`

### Production
```bash
gunicorn "run:app"
```

## Testing

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Frontend tests only
pytest tests/frontend/ -v
```

### Test Structure
```
tests/
├── conftest.py              # Pytest fixtures
├── unit/
│   ├── test_unit_converter.py    # UnitManager tests
│   ├── test_aviation_calculations.py
│   └── test_seo.py
├── integration/
│   ├── test_api.py          # API endpoint tests
│   └── test_routes.py       # Page route tests
└── frontend/
    └── test_frontend.py     # HTML structure & JS integration tests
```

## Project Structure

```
anyunit/
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── routes/
│   │   ├── main.py          # Homepage, sitemap, robots.txt
│   │   ├── converter.py     # Category and conversion pages
│   │   ├── api.py           # JSON conversion API
│   │   ├── aviation.py      # Aviation calculators
│   │   ├── markdown_converter.py
│   │   ├── timezone.py
│   │   └── text_files.py
│   ├── utils/
│   │   ├── unit_converter.py      # UnitManager singleton
│   │   ├── aviation_calculations.py
│   │   └── seo.py                 # Meta tags, JSON-LD
│   ├── templates/
│   │   ├── base.html
│   │   ├── pages/           # Page templates
│   │   ├── aviation/
│   │   └── errors/
│   └── static/
│       ├── css/
│       ├── js/
│       │   ├── converter.js
│       │   ├── quick-converter.js
│       │   └── ...
│       └── data/
│           ├── units.json   # Master unit definitions
│           ├── length.json  # Detailed conversion tables
│           └── ...
├── config.py
├── run.py
├── requirements.txt
└── Procfile
```

## API Reference

### Convert Units
```http
POST /api/convert
Content-Type: application/json

{
  "category": "length",
  "fromUnit": "m",
  "toUnit": "ft",
  "value": 100
}
```

**Response:**
```json
{
  "success": true,
  "result": 328.0839895,
  "formatted": "328.083989"
}
```

### Aviation APIs

#### Fuel Calculator
```http
POST /aviation/api/aviation/fuel-calc
Content-Type: application/json

{
  "distance": 150,
  "indicatedAirspeed": 120,
  "fuelConsumption": 10,
  "windSpeed": 15,
  "windDirection": 270,
  "heading": 90,
  "reserveTime": 45
}
```

**Response:**
```json
{
  "ground_speed": 105.0,
  "flight_time": 85.71,
  "fuel_required": 21.79,
  "reserve_fuel": 7.5
}
```

#### Ground Speed
```http
POST /aviation/api/aviation/ground-speed
Content-Type: application/json

{
  "indicatedAirspeed": 120,
  "windSpeed": 20,
  "windDirection": 180,
  "heading": 0,
  "temperature": 25,
  "pressureAltitude": 5000
}
```

**Response:**
```json
{
  "ground_speed": 112.0,
  "density_altitude": 6200.0,
  "headwind_component": 20.0,
  "crosswind_component": 0.0
}
```

#### Density Altitude
```http
POST /aviation/api/aviation/density-altitude
Content-Type: application/json

{
  "pressureAltitude": 5000,
  "temperature": 30
}
```

**Response:**
```json
{
  "density_altitude": 7000.0
}
```

## URL Structure

| Route | Description |
|-------|-------------|
| `/` | Homepage with category grid |
| `/convert/{category}/` | Category page with all units |
| `/convert/{category}/{from}-to-{to}` | Specific conversion page |
| `/aviation/` | Aviation calculators |
| `/markdown/` | Markdown converter |
| `/time/` | Timezone converter |
| `/text/` | Text file converter |
| `/sitemap.xml` | XML sitemap |
| `/robots.txt` | Robots file |

## SEO Features

- Server-side rendered content
- Semantic HTML structure
- Dynamic meta tags (title, description, canonical URL)
- Open Graph and Twitter Card tags
- JSON-LD structured data (WebSite, BreadcrumbList)
- Auto-generated sitemap.xml
- robots.txt with sitemap reference

## Architecture Notes

### Unit Conversion System
- Units defined in `app/static/data/units.json` with conversion factors relative to a base unit
- Temperature uses explicit formulas (not factors) in `UnitManager._convert_temperature()`
- Detailed conversion tables stored per-category in separate JSON files

### Aviation Calculations
- TAS approximation: `TAS = IAS × (1 + 0.02 × PA/1000)`
- Ground speed: `GS = TAS - headwind_component`
- Density altitude: `DA = PA + 120 × (OAT - ISA_temp)`
- Wind components calculated from relative angle between wind direction and heading

### Blueprint Architecture
Seven Flask blueprints with distinct URL prefixes:
- `main_bp` (`/`) — core pages
- `converter_bp` (`/convert`) — unit conversions
- `api_bp` (`/api`) — JSON API
- `markdown_bp` (`/markdown`) — document conversion
- `timezone_bp` (`/time`) — timezone tools
- `text_files_bp` (`/text`) — file format conversion
- `aviation` (`/aviation`) — aviation calculators

## Deployment

### Heroku
The application includes a `Procfile` for Heroku deployment:
```
web: gunicorn "run:app"
```

Deploy with:
```bash
heroku create
git push heroku main
```

## License

[Add license information]
