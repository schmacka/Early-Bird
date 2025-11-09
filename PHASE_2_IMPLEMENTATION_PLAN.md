# Phase 2 Implementation Plan - Core Features

**Created:** 2025-11-09
**Branch:** `claude/implement-phase-2-plan-011CUxz2xLNd1Wa5FBvsLdvh`
**Estimated Total Effort:** 4-5 development days

---

## Overview

Phase 2 focuses on core features that provide high value with medium implementation effort. These features enhance documentation, visualization, and parental guidance. All features maintain the core principle of using **corrected age** for all calculations and references.

---

## Feature 2.1: Pride Archive (Stolz-Archiv) with Timeline
**Priority:** VERY HIGH | **Effort:** MEDIUM | **Value:** VERY HIGH

### Description
A comprehensive timeline view of all achievements, milestones, and growth records. Allows parents to see their child's complete developmental journey in one place.

### Implementation Details

#### 1. Backend Changes (sensor.py)

**Location:** `early_bird/sensor.py`

Add comprehensive archive retrieval method:

```python
def get_pride_archive(self, filter_category=None, sort_order="desc"):
    """
    Get comprehensive timeline of all achievements and events

    Args:
        filter_category: Optional filter (motor, cognitive, language, life_moments, growth)
        sort_order: "asc" for chronological, "desc" for reverse chronological

    Returns:
        dict: Timeline events with metadata
    """
    events = []

    # Add milestone achievements
    for achievement in self.data.get("milestone_achievements", []):
        events.append({
            "type": "milestone",
            "category": achievement["category"],
            "title": achievement["milestone"],
            "date": achievement["date"],
            "corrected_age_weeks": achievement.get("corrected_age_weeks", 0),
            "notes": achievement.get("notes", ""),
            "icon": self._get_category_icon(achievement["category"])
        })

    # Add growth records
    for record in self.data.get("growth_records", []):
        events.append({
            "type": "growth",
            "category": "growth",
            "title": f"Wachstumsmessung: {record.get('weight_kg', 'N/A')} kg",
            "date": record["date"],
            "corrected_age_weeks": record.get("corrected_age_weeks", 0),
            "notes": f"Größe: {record.get('height_cm', 'N/A')} cm, Kopfumfang: {record.get('head_circumference_cm', 'N/A')} cm",
            "icon": "📏",
            "data": record
        })

    # Add U-examinations if completed
    for exam in self.data.get("u_examinations_records", []):
        events.append({
            "type": "u_examination",
            "category": "health",
            "title": f"{exam['exam_name']} Untersuchung",
            "date": exam["date"],
            "corrected_age_weeks": exam.get("corrected_age_weeks", 0),
            "notes": exam.get("notes", ""),
            "icon": "🏥"
        })

    # Filter by category if requested
    if filter_category:
        events = [e for e in events if e["category"] == filter_category]

    # Sort by date
    events.sort(key=lambda x: x["date"], reverse=(sort_order == "desc"))

    return {
        "events": events,
        "total_count": len(events),
        "categories": self._get_event_categories(events),
        "date_range": self._get_date_range(events)
    }

def _get_category_icon(self, category):
    """Get icon for category"""
    icons = {
        "motor": "🏃",
        "cognitive": "🧠",
        "language": "💬",
        "life_moments": "❤️",
        "growth": "📏",
        "health": "🏥"
    }
    return icons.get(category, "⭐")

def _get_event_categories(self, events):
    """Get unique categories with counts"""
    categories = {}
    for event in events:
        cat = event["category"]
        categories[cat] = categories.get(cat, 0) + 1
    return categories

def _get_date_range(self, events):
    """Get date range of events"""
    if not events:
        return {"start": None, "end": None}

    dates = [datetime.fromisoformat(e["date"]) for e in events]
    return {
        "start": min(dates).isoformat(),
        "end": max(dates).isoformat()
    }

def get_monthly_summary(self, year_month=None):
    """
    Get summary of events for a specific month

    Args:
        year_month: "YYYY-MM" format, defaults to current month

    Returns:
        dict: Monthly achievements and statistics
    """
    if not year_month:
        year_month = datetime.now().strftime("%Y-%m")

    year, month = map(int, year_month.split("-"))

    archive = self.get_pride_archive()
    month_events = [
        e for e in archive["events"]
        if datetime.fromisoformat(e["date"]).year == year
        and datetime.fromisoformat(e["date"]).month == month
    ]

    return {
        "year_month": year_month,
        "events": month_events,
        "count": len(month_events),
        "categories": self._get_event_categories(month_events)
    }
```

#### 2. API Changes (run.py)

**Location:** `early_bird/run.py`

Add endpoints:
```python
@app.route('/api/pride-archive')
def api_pride_archive():
    """Get complete pride archive"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    filter_category = request.args.get('category')
    sort_order = request.args.get('sort', 'desc')

    return jsonify(sensor.get_pride_archive(filter_category, sort_order))

@app.route('/api/pride-archive/monthly/<year_month>')
def api_monthly_summary(year_month):
    """Get monthly summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_monthly_summary(year_month))
```

#### 3. Frontend Changes

**New File:** `early_bird/templates/archive.html`

Create dedicated archive page with timeline visualization, filters, and export options.

**Update:** `early_bird/templates/index.html`

Add link to archive in main navigation.

#### 4. Translations

Add archive-related translations in both languages.

#### 5. Testing

Test timeline sorting, filtering, date range calculations, and empty state handling.

---

## Feature 2.2: Extended Growth Charts (Erweiterte Wachstumskurven)
**Priority:** HIGH | **Effort:** MEDIUM | **Value:** HIGH

### Description
Visual charts displaying weight, height, and head circumference over time with reference percentile curves adjusted for premature babies.

### Implementation Details

#### 1. Backend Changes (sensor.py)

**Location:** `early_bird/sensor.py`

Add chart data preparation methods:

```python
def get_growth_chart_data(self, measurement_type="weight"):
    """
    Get formatted data for growth charts

    Args:
        measurement_type: "weight", "height", or "head_circumference"

    Returns:
        dict: Chart data with labels and values
    """
    records = self.data.get("growth_records", [])

    # Sort by date
    records_sorted = sorted(records, key=lambda x: x["date"])

    labels = []
    values = []
    corrected_ages = []

    field_map = {
        "weight": "weight_kg",
        "height": "height_cm",
        "head_circumference": "head_circumference_cm"
    }

    field = field_map.get(measurement_type, "weight_kg")

    for record in records_sorted:
        if field in record:
            labels.append(record["date"])
            values.append(record[field])
            corrected_ages.append(record.get("corrected_age_weeks", 0))

    return {
        "labels": labels,
        "values": values,
        "corrected_ages": corrected_ages,
        "measurement_type": measurement_type,
        "unit": self._get_measurement_unit(measurement_type),
        "count": len(values)
    }

def _get_measurement_unit(self, measurement_type):
    """Get unit for measurement type"""
    units = {
        "weight": "kg",
        "height": "cm",
        "head_circumference": "cm"
    }
    return units.get(measurement_type, "")

def get_growth_statistics(self):
    """
    Calculate growth statistics

    Returns:
        dict: Growth trends and statistics
    """
    records = self.data.get("growth_records", [])

    if len(records) < 2:
        return {"insufficient_data": True}

    records_sorted = sorted(records, key=lambda x: x["date"])

    # Calculate weight gain
    first_weight = records_sorted[0].get("weight_kg")
    last_weight = records_sorted[-1].get("weight_kg")
    weight_gain = last_weight - first_weight if first_weight and last_weight else None

    # Calculate height gain
    first_height = records_sorted[0].get("height_cm")
    last_height = records_sorted[-1].get("height_cm")
    height_gain = last_height - first_height if first_height and last_height else None

    # Time span
    first_date = datetime.fromisoformat(records_sorted[0]["date"])
    last_date = datetime.fromisoformat(records_sorted[-1]["date"])
    days_span = (last_date - first_date).days
    weeks_span = days_span / 7

    return {
        "weight_gain_total_kg": round(weight_gain, 2) if weight_gain else None,
        "weight_gain_per_week_g": round((weight_gain / weeks_span) * 1000, 1) if weight_gain and weeks_span > 0 else None,
        "height_gain_total_cm": round(height_gain, 1) if height_gain else None,
        "height_gain_per_week_cm": round(height_gain / weeks_span, 2) if height_gain and weeks_span > 0 else None,
        "measurement_count": len(records),
        "time_span_weeks": round(weeks_span, 1),
        "latest_measurement": records_sorted[-1]
    }
```

#### 2. API Changes (run.py)

Add endpoints for chart data:
```python
@app.route('/api/growth/chart/<measurement_type>')
def api_growth_chart(measurement_type):
    """Get growth chart data"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_growth_chart_data(measurement_type))

@app.route('/api/growth/statistics')
def api_growth_statistics():
    """Get growth statistics"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_growth_statistics())
```

#### 3. Frontend Changes

Add Chart.js library and create interactive charts in dashboard.

#### 4. Testing

Test with various data sets, empty data, single record, and calculation accuracy.

---

## Feature 2.3: Sleep Pattern Tracking (Schlafmuster-Tracking)
**Priority:** HIGH | **Effort:** MEDIUM | **Value:** HIGH

### Description
Track sleep times, naps, and patterns. Visualize sleep duration and compare with age-appropriate expectations.

### Implementation Details

#### 1. Backend Changes (sensor.py)

**Location:** `early_bird/sensor.py`

Add sleep tracking functionality:

```python
def add_sleep_record(self, sleep_type, start_time, end_time, quality="normal", notes=""):
    """
    Add sleep record

    Args:
        sleep_type: "night" or "nap"
        start_time: ISO format datetime
        end_time: ISO format datetime
        quality: "poor", "normal", "good"
        notes: Optional notes

    Returns:
        dict: Sleep record with duration calculated
    """
    if "sleep_records" not in self.data:
        self.data["sleep_records"] = []

    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    duration_hours = (end - start).total_seconds() / 3600

    record = {
        "sleep_type": sleep_type,
        "start_time": start_time,
        "end_time": end_time,
        "duration_hours": round(duration_hours, 2),
        "quality": quality,
        "notes": notes,
        "date": start.date().isoformat(),
        "corrected_age_weeks": self._calculate_weeks_from_due()
    }

    self.data["sleep_records"].append(record)
    self._save_data()

    return record

def get_sleep_summary(self, date=None, days_back=7):
    """
    Get sleep summary for date range

    Args:
        date: Target date (ISO format) or None for today
        days_back: Number of days to include

    Returns:
        dict: Sleep statistics and patterns
    """
    if not date:
        date = datetime.now().date().isoformat()

    target_date = datetime.fromisoformat(date).date()
    start_date = target_date - timedelta(days=days_back)

    records = self.data.get("sleep_records", [])

    # Filter records in range
    relevant_records = [
        r for r in records
        if start_date <= datetime.fromisoformat(r["date"]).date() <= target_date
    ]

    if not relevant_records:
        return {"no_data": True}

    # Calculate statistics
    total_sleep_hours = sum(r["duration_hours"] for r in relevant_records)
    night_sleep = [r for r in relevant_records if r["sleep_type"] == "night"]
    naps = [r for r in relevant_records if r["sleep_type"] == "nap"]

    avg_night_sleep = sum(r["duration_hours"] for r in night_sleep) / len(night_sleep) if night_sleep else 0
    avg_naps_per_day = len(naps) / days_back
    avg_total_sleep = total_sleep_hours / days_back

    return {
        "date_range": {
            "start": start_date.isoformat(),
            "end": target_date.isoformat()
        },
        "total_sleep_hours": round(total_sleep_hours, 1),
        "average_sleep_per_day": round(avg_total_sleep, 1),
        "average_night_sleep": round(avg_night_sleep, 1),
        "average_naps_per_day": round(avg_naps_per_day, 1),
        "total_nights": len(night_sleep),
        "total_naps": len(naps),
        "quality_distribution": self._calculate_quality_distribution(relevant_records),
        "age_appropriate_expectations": self._get_sleep_expectations()
    }

def _calculate_quality_distribution(self, records):
    """Calculate distribution of sleep quality"""
    distribution = {"poor": 0, "normal": 0, "good": 0}
    for record in records:
        quality = record.get("quality", "normal")
        distribution[quality] = distribution.get(quality, 0) + 1
    return distribution

def _get_sleep_expectations(self):
    """Get age-appropriate sleep expectations"""
    corrected_weeks = self._calculate_weeks_from_due()

    if corrected_weeks < 6:
        return {
            "total_hours": "16-20",
            "night_hours": "8-10 (mit Unterbrechungen)",
            "naps": "4-5 pro Tag",
            "note": "Neugeborene schlafen viel, aber in kurzen Intervallen"
        }
    elif corrected_weeks < 16:
        return {
            "total_hours": "14-17",
            "night_hours": "9-10",
            "naps": "3-4 pro Tag",
            "note": "Schlafphasen werden allmählich länger"
        }
    elif corrected_weeks < 26:
        return {
            "total_hours": "14-16",
            "night_hours": "10-11",
            "naps": "2-3 pro Tag",
            "note": "Nachtschlaf wird kontinuierlicher"
        }
    elif corrected_weeks < 52:
        return {
            "total_hours": "12-15",
            "night_hours": "11-12",
            "naps": "2 pro Tag",
            "note": "Etablierung eines regelmäßigen Schlafrhythmus"
        }
    else:
        return {
            "total_hours": "11-14",
            "night_hours": "11-12",
            "naps": "1-2 pro Tag",
            "note": "Übergang zu einem Mittagsschlaf"
        }

def get_sleep_records(self, limit=50):
    """Get recent sleep records"""
    records = self.data.get("sleep_records", [])
    records_sorted = sorted(records, key=lambda x: x["start_time"], reverse=True)
    return records_sorted[:limit]
```

#### 2. API Changes (run.py)

Add sleep tracking endpoints:
```python
@app.route('/api/sleep', methods=['POST'])
def api_add_sleep():
    """Add sleep record"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    data = request.json
    record = sensor.add_sleep_record(
        sleep_type=data.get('sleep_type'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        quality=data.get('quality', 'normal'),
        notes=data.get('notes', '')
    )
    return jsonify(record)

@app.route('/api/sleep/summary')
def api_sleep_summary():
    """Get sleep summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    date = request.args.get('date')
    days_back = int(request.args.get('days_back', 7))

    return jsonify(sensor.get_sleep_summary(date, days_back))

@app.route('/api/sleep/records')
def api_sleep_records():
    """Get sleep records"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    limit = int(request.args.get('limit', 50))
    return jsonify({"records": sensor.get_sleep_records(limit)})
```

#### 3. Frontend Changes

Add sleep tracking form and visualization dashboard.

#### 4. Testing

Test duration calculations, time zone handling, edge cases (very short/long sleep), and statistics accuracy.

---

## Feature 2.4: Calming Techniques & Bonding Tips
**Priority:** MEDIUM | **Effort:** LOW-MEDIUM | **Value:** HIGH

### Description
Information pages with practical parenting techniques for calming fussy babies and promoting bonding.

### Implementation Details

#### 1. Frontend Changes

**New File:** `early_bird/templates/calming_techniques.html`

Comprehensive guide with:
- 5 S Method (Swaddle, Side, Shush, Swing, Suck)
- White noise techniques
- Swaddling instructions
- Carrying positions
- Age-appropriate techniques

**New File:** `early_bird/templates/bonding_tips.html`

Bonding guidance with:
- Skin-to-skin contact (Kangaroo care)
- Eye contact and communication
- Responsive parenting
- Baby wearing
- Age-specific interaction ideas

#### 2. Route Addition (run.py)

```python
@app.route('/calming-techniques')
def calming_techniques_page():
    """Calming techniques information page"""
    return render_template('calming_techniques.html', config=config)

@app.route('/bonding-tips')
def bonding_tips_page():
    """Bonding tips information page"""
    return render_template('bonding_tips.html', config=config)
```

#### 3. Translations

Create German and English versions of all content.

#### 4. Testing

Manual testing for content accuracy, mobile responsiveness, and link functionality.

---

## Feature 2.5: Progress Reminders (Fortschritts-Erinnerungen)
**Priority:** MEDIUM | **Effort:** MEDIUM | **Value:** MEDIUM-HIGH

### Description
Weekly/monthly summaries showing progress over time to help parents see how far their child has come.

### Implementation Details

#### 1. Backend Changes (sensor.py)

**Location:** `early_bird/sensor.py`

Add progress tracking:

```python
def get_progress_reminder(self, weeks_back=4):
    """
    Generate progress reminder showing growth over time

    Args:
        weeks_back: How many weeks to look back

    Returns:
        dict: Progress summary with comparisons
    """
    target_date = datetime.now() - timedelta(weeks=weeks_back)

    # Current state
    current_corrected_weeks = self._calculate_weeks_from_due()
    current_ww = self.get_current_wonder_week()

    # Milestones achieved in period
    achievements = [
        a for a in self.data.get("milestone_achievements", [])
        if datetime.fromisoformat(a["date"]) >= target_date
    ]

    # Growth changes
    growth_records = self.data.get("growth_records", [])
    growth_sorted = sorted(growth_records, key=lambda x: x["date"])

    past_record = None
    for record in growth_sorted:
        if datetime.fromisoformat(record["date"]) <= target_date:
            past_record = record

    current_record = growth_sorted[-1] if growth_sorted else None

    growth_change = None
    if past_record and current_record:
        growth_change = {
            "weight_gain_kg": round(current_record.get("weight_kg", 0) - past_record.get("weight_kg", 0), 2),
            "height_gain_cm": round(current_record.get("height_cm", 0) - past_record.get("height_cm", 0), 1),
            "head_gain_cm": round(current_record.get("head_circumference_cm", 0) - past_record.get("head_circumference_cm", 0), 1)
        }

    return {
        "weeks_back": weeks_back,
        "target_date": target_date.isoformat(),
        "current_corrected_age_weeks": current_corrected_weeks,
        "past_corrected_age_weeks": current_corrected_weeks - weeks_back,
        "milestones_achieved_count": len(achievements),
        "milestones_achieved": achievements,
        "growth_change": growth_change,
        "current_wonder_week": current_ww.get("name") if current_ww else None,
        "encouragement": self._get_progress_encouragement(len(achievements), growth_change)
    }

def _get_progress_encouragement(self, milestone_count, growth_change):
    """Generate encouraging message based on progress"""
    messages = []

    if milestone_count > 0:
        messages.append(f"{self.child_name} hat {milestone_count} neue Meilensteine erreicht!")

    if growth_change and growth_change.get("weight_gain_kg", 0) > 0:
        messages.append(f"{self.child_name} ist {growth_change['weight_gain_kg']} kg gewachsen!")

    if growth_change and growth_change.get("height_gain_cm", 0) > 0:
        messages.append(f"{self.child_name} ist {growth_change['height_gain_cm']} cm größer geworden!")

    if not messages:
        messages.append(f"{self.child_name} entwickelt sich stetig weiter - jeder Tag zählt!")

    return " ".join(messages)
```

#### 2. API Changes (run.py)

```python
@app.route('/api/progress-reminder')
def api_progress_reminder():
    """Get progress reminder"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    weeks_back = int(request.args.get('weeks_back', 4))
    return jsonify(sensor.get_progress_reminder(weeks_back))
```

#### 3. Frontend Changes

Add progress reminder card to dashboard with time range selector.

#### 4. Testing

Test with various time ranges, edge cases (no data, no changes), and calculation accuracy.

---

## Implementation Order

### Week 1
1. Feature 2.3: Sleep Pattern Tracking (Day 1-2)
   - Core functionality with immediate value
   - Independent feature, no dependencies

2. Feature 2.5: Progress Reminders (Day 2-3)
   - Leverages existing data structures
   - Motivational value for parents

### Week 2
3. Feature 2.2: Extended Growth Charts (Day 3-4)
   - Visual enhancement of existing growth tracking
   - Requires Chart.js integration

4. Feature 2.1: Pride Archive with Timeline (Day 4-5)
   - Comprehensive feature bringing everything together
   - Depends on other features being complete

### Week 3
5. Feature 2.4: Calming Techniques & Bonding Tips (Day 5-6)
   - Content-focused, less technical
   - Can be done in parallel with testing

---

## Testing Strategy

### Unit Tests (test_sensor.py)
- All new methods in sensor.py
- Edge cases (empty data, single record, time zones)
- Calculation accuracy (sleep duration, growth statistics, progress deltas)

### Integration Tests
- API endpoint responses
- Frontend-backend data flow
- Chart rendering with real data

### Manual Testing
- Sleep tracking with various scenarios
- Growth charts with different data sets
- Timeline filtering and sorting
- Mobile responsiveness
- Browser compatibility

---

## Deployment Checklist

Before pushing to main:
- [ ] All unit tests pass
- [ ] Manual testing completed
- [ ] German translations complete and accurate
- [ ] English translations complete and accurate
- [ ] Chart.js integrated correctly
- [ ] No console errors in browser
- [ ] Mobile layout works correctly
- [ ] Data migration tested (new fields in child_data.json)
- [ ] Performance tested with large datasets
- [ ] Privacy considerations addressed (DSGVO compliance)

---

## Technical Considerations

### Chart.js Integration
- Add Chart.js via CDN or local copy
- Responsive chart configuration
- Color scheme matching Early Bird branding
- Accessibility considerations (screen readers)

### Performance
- Lazy loading for timeline with pagination
- Efficient date range queries
- Caching for statistics calculations
- Optimized chart data preparation

### Data Structure Changes
New fields in `/data/child_data.json`:
- `sleep_records`: Array of sleep tracking entries
- `pride_archive_viewed`: Last viewed timestamp
- `progress_reminders_sent`: History of generated reminders

### Multilingual Content
- All informational pages in German and English
- Culturally appropriate bonding/calming techniques
- Age references using both weeks and months
- Clear language for non-medical audience

---

## Future Enhancements (Phase 3+)

Items identified during planning but deferred:
1. **Export Pride Archive to PDF** → Phase 4
2. **Sleep pattern correlation with Wonder Weeks** → Phase 3
3. **Push notifications for progress reminders** → Phase 3
4. **Percentile curves for growth charts** → Phase 3
5. **Photo attachments to timeline events** → Phase 3

---

## Notes

- All features use **corrected age** (from due_date, not birth_date)
- All features include German and English support
- All health-related content includes appropriate disclaimers
- All features are optional/non-intrusive
- Data privacy: Everything stored locally in `/data/child_data.json`
- No external API calls or cloud storage in Phase 2
- Charts use responsive design for mobile devices
- Timeline pagination recommended for performance with >100 events

---

**End of Implementation Plan**
