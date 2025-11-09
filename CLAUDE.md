# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Early Bird is a Home Assistant addon for tracking premature children's development using corrected age calculations, Wonder Weeks integration, and milestone tracking. All calculations use corrected age (from due date, not birth date) which is critical for premature babies.

## Development Commands

### Testing
```bash
# Run test suite
python3 test_sensor.py

# Test with custom data (modify test_sensor.py dates first)
python3 -c "from early_bird.sensor import EarlyBirdSensor; s = EarlyBirdSensor('Test', '2024-01-01', '2024-03-01'); print(s.get_summary())"
```

### Docker & Deployment
```bash
# Build for local testing (from early_bird/ directory)
docker build -t early-bird-test .

# Run locally for testing
docker run -p 8099:8099 -v /tmp/data:/data early-bird-test

# Access dashboard
# http://localhost:8099
```

### Home Assistant Development
```bash
# Validate config.json schema
python3 -m json.tool early_bird/config.json

# Check translations
python3 -m json.tool early_bird/translations/de.json
python3 -m json.tool early_bird/translations/en.json

# Verify installation script
bash verify_installation.sh
```

## Architecture

### Two-Component Design

1. **sensor.py** (Core Logic Layer)
   - Pure Python class with no Flask/web dependencies
   - All age calculations, Wonder Weeks logic, and milestone tracking
   - JSON file-based persistence (`/data/child_data.json`)
   - Can be imported and tested independently

2. **run.py** (Web Interface Layer)
   - Flask application providing REST API and web dashboard
   - Loads configuration from `/data/options.json` (Home Assistant managed)
   - Initializes EarlyBirdSensor with config
   - All routes delegate to sensor methods

### Data Flow

```
Home Assistant Config
    ↓ (writes to /data/options.json)
run.py (Flask)
    ↓ (initializes)
EarlyBirdSensor
    ↓ (reads/writes)
/data/child_data.json
```

### Key Architectural Principles

**Corrected Age is Fundamental**: Every calculation, milestone, and Wonder Week uses corrected age (weeks from due_date), not actual age (weeks from birth_date). This is the core value proposition for premature baby tracking.

**Date Calculations**:
- `self.due_date`: The reference point for all corrected age calculations
- `self.birth_date`: Used only to calculate prematurity and actual age
- Current date from `datetime.now()`: Used to calculate ages
- Formula: `corrected_age = today - due_date` (NOT `today - birth_date`)

**Data Storage**:
- Configuration: `/data/options.json` (managed by Home Assistant)
- User data: `/data/child_data.json` (managed by sensor.py)
- Growth records and milestone achievements stored as JSON arrays
- All dates stored in ISO format, ages stored as week counts

**Stateless Sensor**: EarlyBirdSensor loads data from JSON on each request. No in-memory state management. This ensures data consistency across container restarts.

## Critical Constants

### Wonder Weeks (sensor.py:15-26)
10 developmental leaps defined as weeks from due date. When adding leaps, maintain chronological order and include name + duration.

### Milestones (sensor.py:29-56)
Three categories (motor, cognitive, language) with age_weeks from due date. These are evidence-based developmental expectations adjusted for prematurity.

## API Contract

All 8 REST endpoints return JSON. Key endpoints:

- `GET /api/summary`: Complete overview (includes age, Wonder Week, upcoming milestones, counts)
- `GET /api/age`: Both corrected and actual age in years/months/weeks/days plus prematurity
- `POST /api/growth`: Requires `weight_kg`, `height_cm`, optional `head_circumference_cm`
- `POST /api/milestone-achievements`: Requires `category` (motor/cognitive/language) and `milestone`

## Template System

Templates use Jinja2 and expect:
- `config` object with child_name, language, notifications_enabled
- JavaScript fetches from `/api/summary` on page load
- Auto-refresh every 60 seconds for age display

Language selection in templates uses `config.language` ('de' or 'en').

## Home Assistant Integration

**Ingress**: The addon uses Home Assistant ingress (ingress: true, ingress_port: 8099) allowing access without exposing ports. Users access via Supervisor panel, not direct URL.

**Configuration Schema**: Defined in config.json. All fields except child_name are required for sensor initialization. Missing birth_date or due_date causes sensor to be None, showing setup.html.

**Multi-Architecture**: Supports armhf, armv7, aarch64, amd64, i386 via build.json configuration.

## Common Development Patterns

### Adding a New Milestone Category
1. Add category to MILESTONES dict in sensor.py with age_weeks entries
2. Update get_upcoming_milestones() to include new category
3. Update POST /api/milestone-achievements validation in run.py
4. Add translations in de.json and en.json

### Adding a New Wonder Week
1. Add entry to WONDER_WEEKS list in chronological order
2. No code changes needed (get_current_wonder_week() iterates the list)
3. Add translations for leap name if needed

### Modifying Age Calculations
Always use `self.due_date` as the reference for corrected age. The birth_date is only used for:
- Calculating prematurity (due_date - birth_date)
- Calculating actual age for display purposes
- Never for milestone or Wonder Week timing

## Testing Guidance

test_sensor.py uses synthetic dates (2024-01-01 birth, 2024-02-26 due = 8 weeks premature). When writing new tests:
- Use similar synthetic dates in the past
- Test both corrected and actual age calculations
- Verify data persists to /tmp/test_data.json
- Clean up test file after completion

## File Locations Matter

- Configuration: `/data/options.json` (read-only from addon perspective)
- User data: `/data/child_data.json` (read-write by sensor)
- Templates: `templates/` directory relative to run.py
- Translations: `translations/` directory relative to run.py
- Static assets: `www/` directory (currently unused)

## Translation Keys

When adding UI elements, add translations to both de.json and en.json. German is the primary language (default). Translation structure is nested by section (age, wonder_weeks, milestones, growth, etc.).
