# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run production server (Heroku-style)
gunicorn "run:app"

# Set environment variables (optional, has defaults)
export SECRET_KEY="your-secret-key"
export DEBUG=true

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run single test file
pytest tests/unit/test_unit_converter.py -v

# Run single test
pytest tests/unit/test_unit_converter.py::TestConvertValue::test_length_conversion_meter_to_foot -v
```

## Architecture Overview

### Application Structure

Flask app factory pattern in `app/__init__.py`. Seven blueprints registered with distinct URL prefixes:

| Blueprint | Prefix | Purpose |
|-----------|--------|---------|
| `main_bp` | `/` | Homepage, robots.txt, sitemap.xml, privacy |
| `converter_bp` | `/convert` | Category and conversion pages |
| `api_bp` | `/api` | JSON conversion API |
| `markdown_bp` | `/markdown` | Markdown to DOCX/HTML converter |
| `timezone_bp` | `/time` | Timezone utilities |
| `text_files_bp` | `/text` | Text file tools |
| `aviation` | `/aviation` | Aviation calculators |

### Data Layer

No database. Static JSON files in `app/static/data/`:
- `units.json` — master unit definitions with categories, factors, and popular conversions
- `{category}.json` — detailed conversion tables per category (length.json, weight.json, etc.)
- `timezones.json` — timezone data

### Core Logic

- **`app/utils/unit_converter.py`** — `UnitManager` singleton handles all unit conversions using factor-based math; temperature uses explicit formulas
- **`app/utils/aviation_calculations.py`** — fuel requirements, ground speed (TAS ≈ IAS × (1 + 0.02 × PA/1000)), density altitude
- **`app/utils/seo.py`** — generates meta tags, canonical URLs, JSON-LD structured data

### Frontend

- Templates: Jinja2 in `app/templates/` (base.html, pages/, components/)
- Assets: `app/static/css/`, `app/static/js/`
- Bootstrap 5, vanilla JS with real-time client-side conversions via `quick-converter.js`

### Key API Endpoints

```
POST /api/convert
  Body: { "category": str, "fromUnit": str, "toUnit": str, "value": number }
  Returns: { success, result, formatted }

POST /aviation/api/aviation/fuel-calc
POST /aviation/api/aviation/ground-speed
POST /aviation/api/aviation/density-altitude
```

## Task Execution Strategy

### Context Optimization
Extensively use tasks and subtasks (Task tool) to optimize the context usage.

### Parallel Execution
Extensively use parallel tasks and subtasks (multiple Task tools running in the same message) to make the work be done much faster.

### Map-Reduce Approach
Use map-reduce approach with parallel tasks and subtasks.

### Task Reporting
Ensure each task or subtask reports back a very brief explanation on what was done, and what still needs to be done (if any).

### Problem Resolution
Ensure that in case of any problem that task or subtask experiences, it **must** spawn another [set of] subtask(s) to do necessary research and/or experiments in order to resolve the issue.

### Planning and Tracking
Extensively use planning (with TodoWrite tool), so all work is being thoroughly and reliably tracked, and nothing is skipped or lost.

### Parallelization Limits
The maximum number of tasks or subtasks running in parallel should not be more than CPU cores on this machine.

## Software Engineering Principles

### SOLID Principles
You must religiously follow SOLID principles:
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### Additional Principles
- **KISS** (Keep It Simple, Stupid)
- **DRY** (Don't Repeat Yourself)
- **YAGNI** (You Aren't Gonna Need It)
- **TRIZ** (Theory of Inventive Problem Solving)

## Development Process

### Test-Driven Development (TDD)
You must religiously follow TDD (Test-Driven Development) process:
1. Write failing test first
2. Write minimal code to pass
3. Refactor while keeping tests green

### Testing Requirements
You must create both unit tests and integration tests.

### Type Safety
You must do the code as strongly-typed as possible, and even more, so we can find errors **before** we run code in production.

### Linting
You **must** extensively and exhaustively run applicable linters every time before sending code to github.

### Code Review
You must review the changes made with a separate subtask.
