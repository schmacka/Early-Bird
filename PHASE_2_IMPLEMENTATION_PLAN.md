# Phase 2 Implementation Plan - Early Bird

**Created:** 2025-11-09
**Target:** Core Features (High Value, Medium Effort)
**Branch:** `claude/plan-phase-2-roadmap-011CUxyfqXGEZfVUNmFidYC7`

---

## Overview

Phase 2 focuses on core features that provide significant value to parents while maintaining moderate development complexity. All features must work with **corrected age** and support bilingual operation (German/English).

### Phase 2 Features
1. **Stolz-Archiv** (Pride Archive) with Timeline
2. **Erweiterte Wachstumskurven** (Extended Growth Charts)
3. **Schlafmuster-Tracking** (Sleep Pattern Tracking)
4. **Beruhigungstechniken & Bindungstipps** (Calming & Bonding Tips)
5. **Fortschritts-Erinnerungen** (Progress Reminders)

---

## 2.1 Stolz-Archiv (Pride Archive) with Timeline

### Description
A comprehensive view of all achieved milestones presented as a timeline, allowing parents to see their child's development journey at a glance.

### User Stories
- As a parent, I want to see all my child's achievements in chronological order
- As a parent, I want to filter milestones by category (motor, cognitive, language, life_moments)
- As a parent, I want to see statistics about how many milestones we've achieved
- As a parent, I want to export a PDF report of achievements for doctor visits

### Technical Implementation

#### Backend (sensor.py)
```python
# New methods to add:

def get_pride_archive(self, filter_category=None, sort_order='desc'):
    """
    Returns all milestone achievements in timeline format

    Args:
        filter_category: Optional filter (motor, cognitive, language, life_moments)
        sort_order: 'desc' (newest first) or 'asc' (oldest first)

    Returns:
        List of achievements with metadata:
        {
            'category': str,
            'milestone': str,
            'achieved_at': ISO date,
            'age_at_achievement': {weeks, days},
            'corrected_age_weeks': int
        }
    """
    pass

def get_achievement_statistics(self):
    """
    Returns statistics about achievements

    Returns:
        {
            'total_achievements': int,
            'by_category': {
                'motor': int,
                'cognitive': int,
                'language': int,
                'life_moments': int
            },
            'this_week': int,
            'this_month': int,
            'first_achievement_date': ISO date,
            'most_recent_achievement_date': ISO date
        }
    """
    pass
```

#### API Endpoints (run.py)
```python
# New routes to add:

@app.route('/api/pride-archive', methods=['GET'])
def get_pride_archive():
    """
    GET /api/pride-archive?category=motor&sort=desc

    Query params:
        - category: Optional filter (motor, cognitive, language, life_moments)
        - sort: 'desc' or 'asc'

    Returns: JSON with achievements array and statistics
    """
    pass

@app.route('/api/pride-stats', methods=['GET'])
def get_pride_statistics():
    """
    GET /api/pride-stats

    Returns: JSON with achievement statistics
    """
    pass

@app.route('/pride-archive')
def pride_archive_page():
    """
    Renders the Pride Archive page
    """
    pass
```

#### UI Components (templates/pride_archive.html)
- **Header**: "Stolz-Archiv" / "Pride Archive" with child name
- **Statistics Card**: Total achievements, breakdown by category
- **Filter Bar**: Category filter buttons (All, Motor, Cognitive, Language, Life Moments)
- **Timeline Component**:
  - Vertical timeline with date markers
  - Achievement cards with category icon, milestone name, age at achievement
  - Color-coded by category
  - Expandable for future photo/video support
- **Export Button**: "Als PDF exportieren" / "Export as PDF" (basic implementation)

#### Styling Considerations
- Use a vertical timeline design with alternating left/right cards
- Category color scheme:
  - Motor: Blue (#4A90E2)
  - Cognitive: Green (#7ED321)
  - Language: Orange (#F5A623)
  - Life Moments: Purple (#9013FE)
- Responsive design: Stack vertically on mobile
- Smooth scrolling and animations

#### Translation Keys (de.json / en.json)
```json
{
  "pride_archive": {
    "title": "Stolz-Archiv / Pride Archive",
    "subtitle": "Alle erreichten Meilensteine / All achieved milestones",
    "stats": {
      "total": "Gesamt erreichte Meilensteine / Total achievements",
      "motor": "Motorik / Motor skills",
      "cognitive": "Kognition / Cognitive",
      "language": "Sprache / Language",
      "life_moments": "Besondere Momente / Life moments",
      "this_week": "Diese Woche / This week",
      "this_month": "Diesen Monat / This month"
    },
    "filters": {
      "all": "Alle / All",
      "motor": "Motorik / Motor",
      "cognitive": "Kognition / Cognitive",
      "language": "Sprache / Language",
      "life_moments": "Momente / Moments"
    },
    "timeline": {
      "achieved_at_age": "Erreicht mit / Achieved at",
      "weeks": "Wochen / weeks",
      "days": "Tagen / days"
    },
    "export": {
      "button": "Als PDF exportieren / Export as PDF",
      "filename": "stolz-archiv-{child_name} / pride-archive-{child_name}"
    },
    "empty": {
      "title": "Noch keine Meilensteine erreicht / No milestones achieved yet",
      "message": "Füge Meilensteine auf der Hauptseite hinzu / Add milestones on the main page"
    }
  }
}
```

#### Testing Requirements
- Test with 0 achievements (empty state)
- Test with achievements across all categories
- Test filtering by each category
- Test sorting (ascending/descending)
- Test statistics calculations
- Test with both German and English language settings
- Test responsive layout on mobile

---

## 2.2 Erweiterte Wachstumskurven (Extended Growth Charts)

### Description
Interactive charts showing weight, height, and head circumference over time with percentile curves adjusted for premature babies.

### User Stories
- As a parent, I want to see my child's growth visualized over time
- As a parent, I want to compare my child's growth to percentile norms
- As a parent, I want to select different time ranges (1 month, 3 months, 1 year, all)
- As a parent, I want to export charts as images for doctor appointments

### Technical Implementation

#### Backend (sensor.py)
```python
# Constants to add:
# WHO/CDC percentile data adjusted for premature babies
# This is reference data - needs to be researched and added
GROWTH_PERCENTILES = {
    'weight': {
        # age_weeks: {p3: kg, p10: kg, p25: kg, p50: kg, p75: kg, p90: kg, p97: kg}
    },
    'height': {
        # age_weeks: {p3: cm, p10: cm, p25: cm, p50: cm, p75: cm, p90: cm, p97: cm}
    },
    'head_circumference': {
        # age_weeks: {p3: cm, p10: cm, p25: cm, p50: cm, p75: cm, p90: cm, p97: cm}
    }
}

# New methods:

def get_growth_data_for_chart(self, metric='weight', time_range='all'):
    """
    Returns growth data formatted for Chart.js

    Args:
        metric: 'weight', 'height', or 'head_circumference'
        time_range: 'month' (30 days), 'quarter' (90 days), 'year' (365 days), 'all'

    Returns:
        {
            'labels': [ISO dates],
            'actual_data': [values],
            'percentiles': {
                'p3': [values],
                'p10': [values],
                'p25': [values],
                'p50': [values],
                'p75': [values],
                'p90': [values],
                'p97': [values]
            },
            'unit': 'kg' or 'cm'
        }
    """
    pass

def calculate_current_percentile(self, metric, value):
    """
    Calculates which percentile the child is currently in

    Args:
        metric: 'weight', 'height', or 'head_circumference'
        value: Current measurement

    Returns:
        Percentile rank (int) or None if not enough data
    """
    pass
```

#### API Endpoints (run.py)
```python
# New routes:

@app.route('/api/growth-chart/<metric>', methods=['GET'])
def get_growth_chart(metric):
    """
    GET /api/growth-chart/weight?range=quarter
    GET /api/growth-chart/height?range=all
    GET /api/growth-chart/head_circumference?range=month

    Query params:
        - range: 'month', 'quarter', 'year', 'all' (default: 'all')

    Returns: JSON formatted for Chart.js
    """
    pass

@app.route('/growth-charts')
def growth_charts_page():
    """
    Renders the growth charts page
    """
    pass
```

#### UI Components (templates/growth_charts.html)
- **Header**: "Wachstumskurven" / "Growth Charts"
- **Tab Navigation**: Switch between Weight, Height, Head Circumference
- **Time Range Selector**: Buttons for 1M, 3M, 1Y, All
- **Chart Canvas**: Large responsive chart area
- **Legend**:
  - Actual measurements (bold line)
  - Percentile lines (P3, P10, P25, P50, P75, P90, P97 in different colors)
- **Current Stats Card**:
  - Latest measurement
  - Current percentile
  - Change from last measurement
- **Export Button**: Download chart as PNG

#### JavaScript Integration
```javascript
// Use Chart.js library
// CDN: https://cdn.jsdelivr.net/npm/chart.js

function loadGrowthChart(metric, timeRange) {
    fetch(`/api/growth-chart/${metric}?range=${timeRange}`)
        .then(response => response.json())
        .then(data => {
            // Render chart with Chart.js
            const ctx = document.getElementById('growthChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: 'Actual / Tatsächlich',
                            data: data.actual_data,
                            borderColor: '#FF6384',
                            borderWidth: 3,
                            fill: false
                        },
                        // ... percentile datasets
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    // ... chart options
                }
            });
        });
}
```

#### Translation Keys
```json
{
  "growth_charts": {
    "title": "Wachstumskurven / Growth Charts",
    "tabs": {
      "weight": "Gewicht / Weight",
      "height": "Größe / Height",
      "head_circumference": "Kopfumfang / Head Circumference"
    },
    "time_range": {
      "month": "1 Monat / 1 Month",
      "quarter": "3 Monate / 3 Months",
      "year": "1 Jahr / 1 Year",
      "all": "Gesamt / All"
    },
    "percentiles": {
      "label": "Perzentilen / Percentiles",
      "p3": "3. Perzentil",
      "p50": "50. Perzentil (Median)",
      "p97": "97. Perzentil"
    },
    "current_stats": {
      "title": "Aktuelle Werte / Current Values",
      "latest": "Neuester Wert / Latest",
      "percentile": "Perzentil / Percentile",
      "change": "Veränderung / Change"
    },
    "export": "Diagramm exportieren / Export Chart",
    "empty": "Noch keine Wachstumsdaten / No growth data yet"
  }
}
```

#### Data Source Note
**IMPORTANT**: Percentile data must be sourced from reputable medical sources:
- WHO Growth Standards for Children
- Fenton Preterm Growth Charts (specifically for premature babies)
- Need to implement data interpolation for weeks between data points

#### Testing Requirements
- Test with 0, 1, 2, and many growth records
- Test all three metrics (weight, height, head circumference)
- Test all time ranges
- Verify percentile calculations are accurate
- Test chart rendering on different screen sizes
- Test export functionality

---

## 2.3 Schlafmuster-Tracking (Sleep Pattern Tracking)

### Description
Comprehensive sleep tracking to help parents understand their baby's sleep patterns and compare them to age-appropriate norms.

### User Stories
- As a parent, I want to log when my baby falls asleep and wakes up
- As a parent, I want to see total sleep duration per day
- As a parent, I want to distinguish between nighttime sleep and naps
- As a parent, I want to see if my baby's sleep is typical for their corrected age

### Technical Implementation

#### Backend (sensor.py)
```python
# Constants to add:
TYPICAL_SLEEP_PATTERNS = {
    # Corrected age in weeks: {total_hours, num_naps, night_hours}
    0: {'total_hours': (16, 20), 'num_naps': (6, 8), 'night_hours': (8, 10)},
    4: {'total_hours': (14, 17), 'num_naps': (4, 6), 'night_hours': (9, 11)},
    8: {'total_hours': (14, 16), 'num_naps': (3, 5), 'night_hours': (10, 12)},
    12: {'total_hours': (13, 15), 'num_naps': (3, 4), 'night_hours': (10, 12)},
    24: {'total_hours': (12, 14), 'num_naps': (2, 3), 'night_hours': (10, 12)},
    52: {'total_hours': (11, 14), 'num_naps': (1, 2), 'night_hours': (10, 12)}
}

# Data structure in child_data.json:
{
    "sleep_log": [
        {
            "id": "unique_id",
            "sleep_time": "2025-11-09T19:30:00",
            "wake_time": "2025-11-09T23:45:00",
            "sleep_type": "night" or "nap",
            "duration_minutes": 255,
            "notes": "optional notes"
        }
    ]
}

# New methods:

def add_sleep_entry(self, sleep_time, wake_time, sleep_type, notes=""):
    """
    Logs a sleep session

    Args:
        sleep_time: ISO datetime string
        wake_time: ISO datetime string
        sleep_type: 'night' or 'nap'
        notes: Optional notes

    Returns:
        Success status and entry ID
    """
    pass

def get_sleep_patterns(self, days=7):
    """
    Returns sleep pattern analysis for recent days

    Args:
        days: Number of days to analyze (default 7)

    Returns:
        {
            'daily_totals': [
                {
                    'date': ISO date,
                    'total_sleep_minutes': int,
                    'night_sleep_minutes': int,
                    'nap_count': int,
                    'nap_minutes': int
                }
            ],
            'averages': {
                'avg_total_hours': float,
                'avg_nap_count': float,
                'avg_night_hours': float
            },
            'typical_for_age': TYPICAL_SLEEP_PATTERNS entry,
            'comparison': {
                'within_normal': bool,
                'message': str
            }
        }
    """
    pass

def delete_sleep_entry(self, entry_id):
    """
    Removes a sleep entry
    """
    pass
```

#### API Endpoints (run.py)
```python
# New routes:

@app.route('/api/sleep-log', methods=['POST'])
def add_sleep_log():
    """
    POST /api/sleep-log
    Body: {
        "sleep_time": "2025-11-09T19:30:00",
        "wake_time": "2025-11-09T23:45:00",
        "sleep_type": "night" or "nap",
        "notes": "optional"
    }

    Returns: Success status and entry
    """
    pass

@app.route('/api/sleep-log/<entry_id>', methods=['DELETE'])
def delete_sleep_log(entry_id):
    """
    DELETE /api/sleep-log/{id}

    Returns: Success status
    """
    pass

@app.route('/api/sleep-patterns', methods=['GET'])
def get_sleep_patterns():
    """
    GET /api/sleep-patterns?days=7

    Query params:
        - days: Number of days to analyze (default 7)

    Returns: Sleep pattern analysis JSON
    """
    pass

@app.route('/sleep-tracking')
def sleep_tracking_page():
    """
    Renders sleep tracking page
    """
    pass
```

#### UI Components
**Option 1: Add to main dashboard as expandable section**
- "Schlafmuster" / "Sleep Patterns" card
- Quick log form (sleep time, wake time, type selector)
- Mini chart showing last 7 days
- Link to detailed view

**Option 2: Dedicated page (templates/sleep_tracking.html)**
- **Header**: "Schlafmuster-Tracking" / "Sleep Pattern Tracking"
- **Quick Log Form**:
  - Sleep time input (datetime picker)
  - Wake time input (datetime picker)
  - Type selector (Night / Nap)
  - Notes field (optional)
  - Submit button
- **Recent Entries**: List of last 10 entries with delete option
- **Analysis Section**:
  - Chart showing daily sleep totals (Chart.js bar chart)
  - Stats card: Avg total sleep, avg naps, avg night sleep
  - Comparison with typical patterns for corrected age
  - Color-coded indicator: Green (within normal), Yellow (borderline), Red (consult doctor)
- **Time Range Selector**: Last 7 days, 14 days, 30 days

#### Translation Keys
```json
{
  "sleep_tracking": {
    "title": "Schlafmuster / Sleep Patterns",
    "log_form": {
      "title": "Schlaf eintragen / Log Sleep",
      "sleep_time": "Einschlafzeit / Sleep Time",
      "wake_time": "Aufwachzeit / Wake Time",
      "sleep_type": "Art / Type",
      "night": "Nachtschlaf / Night Sleep",
      "nap": "Nickerchen / Nap",
      "notes": "Notizen (optional) / Notes (optional)",
      "submit": "Eintragen / Log"
    },
    "recent_entries": {
      "title": "Letzte Einträge / Recent Entries",
      "duration": "Dauer / Duration",
      "delete": "Löschen / Delete"
    },
    "analysis": {
      "title": "Schlafmuster-Analyse / Sleep Pattern Analysis",
      "daily_total": "Gesamtschlaf pro Tag / Total Sleep per Day",
      "averages": "Durchschnittswerte / Averages",
      "avg_total": "Ø Gesamtschlaf / Avg Total Sleep",
      "avg_naps": "Ø Nickerchen / Avg Naps",
      "avg_night": "Ø Nachtschlaf / Avg Night Sleep",
      "typical_for_age": "Typisch für korrigiertes Alter / Typical for Corrected Age",
      "within_normal": "Im Normbereich / Within Normal Range",
      "consult_doctor": "Bei Unsicherheit Kinderarzt konsultieren / Consult pediatrician if unsure"
    },
    "time_range": {
      "week": "7 Tage / 7 Days",
      "two_weeks": "14 Tage / 14 Days",
      "month": "30 Tage / 30 Days"
    },
    "empty": "Noch keine Schlafdaten / No sleep data yet"
  }
}
```

#### Validation Rules
- Wake time must be after sleep time
- Sleep duration should be reasonable (< 24 hours)
- Datetime must be in the past (can't log future sleep)
- Sleep type must be 'night' or 'nap'

#### Testing Requirements
- Test adding sleep entries (night and nap)
- Test with overlapping sleep times
- Test deletion of entries
- Test pattern analysis with various sleep amounts
- Test comparison with typical patterns across different corrected ages
- Test edge cases (very short sleep, very long sleep)
- Test with empty data

---

## 2.4 Beruhigungstechniken & Bindungstipps (Calming & Bonding Tips)

### Description
Static information pages providing evidence-based techniques for calming babies and promoting bonding, with step-by-step instructions.

### User Stories
- As a parent, I want to learn calming techniques for when my baby is fussy
- As a parent, I want to understand different bonding methods
- As a parent, I want step-by-step instructions I can follow
- As a parent, I want to access this information quickly during stressful moments

### Technical Implementation

#### Content Structure
Create two separate information pages with structured content:

**Calming Techniques Content:**
1. **5 S-Methode** (5 S's Method - Dr. Harvey Karp)
   - Swaddle (Pucken)
   - Side/Stomach Position (Seitenlage)
   - Shush (Weißes Rauschen)
   - Swing (Schaukeln)
   - Suck (Saugen)
   - Step-by-step for each

2. **Pucken** (Swaddling)
   - Benefits
   - How to do it safely
   - When to stop
   - Visual guide

3. **Weißes Rauschen** (White Noise)
   - Why it works
   - Safe volume levels
   - Apps/devices recommendations

4. **Tragetuch-Techniken** (Baby Wearing)
   - Benefits for calming
   - Safe positions
   - Duration recommendations

5. **Rhythmisches Wiegen** (Rhythmic Rocking)
   - Techniques
   - Safe practices

**Bonding Techniques Content:**
1. **Känguruhen** (Kangaroo Care / Skin-to-Skin)
   - Benefits (especially for preemies)
   - How to do it
   - Duration and frequency
   - Both parents can do it

2. **Blickkontakt & Ansprache** (Eye Contact & Talking)
   - Importance for development
   - Age-appropriate interaction
   - Language development

3. **Tragen und Nähe** (Carrying & Closeness)
   - Benefits of babywearing
   - Different carrying methods
   - Building secure attachment

4. **Phasengerechte Interaktionsideen** (Age-Appropriate Interaction)
   - By corrected age phase
   - Activities and games
   - What to expect

#### API Endpoints (run.py)
```python
# New routes:

@app.route('/calming-techniques')
def calming_techniques_page():
    """
    Renders calming techniques information page
    """
    return render_template('calming_techniques.html', config=get_config())

@app.route('/bonding-tips')
def bonding_tips_page():
    """
    Renders bonding tips information page
    """
    return render_template('bonding_tips.html', config=get_config())

# Add links in main dashboard navigation
```

#### UI Components (templates/calming_techniques.html)
- **Header**: "Beruhigungstechniken" / "Calming Techniques"
- **Quick Access Menu**: Jump links to each technique
- **Technique Cards**: Each technique in expandable accordion format
  - Title with icon
  - Brief description
  - Detailed steps (numbered list)
  - "Wichtig" / "Important" callout boxes for safety notes
  - Optional: Embedded video links (external)
- **Disclaimer**: "Diese Informationen ersetzen keine medizinische Beratung"
- **Emergency Note**: "Bei anhaltendem Schreien (>3 Stunden) oder Unsicherheit Kinderarzt kontaktieren"

#### UI Components (templates/bonding_tips.html)
- **Header**: "Bindung stärken" / "Building Bonds"
- **Introduction**: Brief explanation of bonding importance for preemies
- **Technique Cards**: Similar accordion structure
- **Age-Specific Tips**: Section showing techniques appropriate for current corrected age
- **Partner Involvement**: Tips for involving both parents/caregivers

#### Styling
- Clean, readable layout with plenty of white space
- Icons for each technique (calming: 🤱, bonding: 💙)
- Collapsible sections to avoid overwhelming information
- Mobile-optimized (parents may read on phone while holding baby)
- Print-friendly CSS option

#### Translation Keys
```json
{
  "calming_techniques": {
    "title": "Beruhigungstechniken / Calming Techniques",
    "subtitle": "Bewährte Methoden für unruhige Phasen / Proven methods for fussy periods",
    "disclaimer": "Diese Informationen ersetzen keine medizinische Beratung / This information does not replace medical advice",
    "emergency": "Bei anhaltendem Schreien oder Unsicherheit Kinderarzt kontaktieren / Contact pediatrician for persistent crying or concerns",
    "techniques": {
      "five_s": {
        "title": "5 S-Methode (Dr. Harvey Karp) / 5 S's Method",
        "description": "Bewährte Technik zur Beruhigung / Proven calming technique",
        "swaddle": {
          "title": "Swaddle (Pucken) / Swaddling",
          "steps": ["...", "..."]
        }
        // ... more techniques
      }
    }
  },
  "bonding_tips": {
    "title": "Bindung stärken / Building Bonds",
    "subtitle": "Nähe und Verbundenheit aufbauen / Creating closeness and connection",
    "intro": "Bindung ist besonders wichtig für Frühgeborene / Bonding is especially important for premature babies",
    "techniques": {
      "kangaroo_care": {
        "title": "Känguruhen / Kangaroo Care",
        "benefits": ["...", "..."],
        "how_to": ["...", "..."],
        "duration": "Mindestens 1 Stunde / At least 1 hour"
      }
      // ... more techniques
    }
  }
}
```

#### Content Sources
- Reference reputable sources (WHO, AAP, AWMF guidelines)
- Especially focus on preemie-specific considerations
- Include citations where appropriate
- Regular content review for updated guidelines

#### Testing Requirements
- Test both pages render correctly in both languages
- Test navigation between pages
- Test on mobile devices (primary use case)
- Verify all links work (especially external video links)
- Test accordion/collapsible functionality
- Test print CSS

---

## 2.5 Fortschritts-Erinnerungen (Progress Reminders)

### Description
Automated summaries that show parents how far their child has come, providing motivation and perspective during challenging times.

### User Stories
- As a parent, I want to see a summary of this week's achievements
- As a parent, I want to be reminded of progress from weeks/months ago
- As a parent, I want to see visualized progress over time
- As a parent, I want this to appear regularly without having to request it

### Technical Implementation

#### Backend (sensor.py)
```python
# New methods:

def get_progress_reminder(self, period='week'):
    """
    Generates a progress reminder for specified period

    Args:
        period: 'week', 'month', or 'quarter'

    Returns:
        {
            'period': str,
            'date_range': {
                'start': ISO date,
                'end': ISO date
            },
            'achievements': [
                {
                    'category': str,
                    'milestone': str,
                    'achieved_at': ISO date
                }
            ],
            'growth_changes': {
                'weight_change_kg': float,
                'height_change_cm': float
            },
            'comparison': {
                'corrected_age_then': int (weeks),
                'corrected_age_now': int (weeks),
                'message': str  # e.g., "4 Wochen ago, {name} couldn't roll over. Now they can!"
            },
            'motivational_message': str
        }
    """
    pass

def get_before_after_milestones(self, weeks_ago=4):
    """
    Compares capabilities from X weeks ago to now

    Args:
        weeks_ago: How many weeks to look back

    Returns:
        {
            'weeks_ago': int,
            'date_then': ISO date,
            'capabilities_gained': [milestone names],
            'comparison_message': str
        }
    """
    pass

def get_milestone_velocity(self):
    """
    Calculates rate of milestone achievements

    Returns:
        {
            'last_week': int,
            'last_month': int,
            'last_quarter': int,
            'trend': 'increasing', 'steady', or 'decreasing'
        }
    """
    pass
```

#### Constants to Add
```python
MOTIVATIONAL_MESSAGES = {
    'de': [
        "Jeder kleine Schritt ist ein großer Erfolg!",
        "Du machst das großartig, {child_name} entwickelt sich wunderbar!",
        "Schau, wie weit {child_name} schon gekommen ist!",
        "Frühchen brauchen Zeit - und {child_name} macht das toll!",
        "Jeder Meilenstein ist ein Grund zum Feiern!",
        "Du bist genau die richtige Mama/Papa für {child_name}!",
        # ... more messages
    ],
    'en': [
        "Every small step is a big success!",
        "You're doing great, {child_name} is developing wonderfully!",
        "Look how far {child_name} has come!",
        "Preemies need time - and {child_name} is doing great!",
        "Every milestone is a reason to celebrate!",
        "You're exactly the right parent for {child_name}!",
        # ... more messages
    ]
}
```

#### API Endpoints (run.py)
```python
# New routes:

@app.route('/api/progress-reminder', methods=['GET'])
def get_progress_reminder():
    """
    GET /api/progress-reminder?period=week

    Query params:
        - period: 'week', 'month', 'quarter' (default: 'week')

    Returns: Progress reminder JSON
    """
    pass

@app.route('/api/before-after', methods=['GET'])
def get_before_after():
    """
    GET /api/before-after?weeks=4

    Query params:
        - weeks: How many weeks to look back (default: 4)

    Returns: Before/after comparison JSON
    """
    pass
```

#### UI Components

**Option 1: Dashboard Widget**
Add prominent card to main dashboard (templates/index.html):

```html
<!-- Progress Reminder Widget -->
<div class="card progress-reminder">
    <div class="card-header">
        <h3>🎉 Diese Woche / This Week</h3>
    </div>
    <div class="card-body">
        <!-- Achievements count -->
        <div class="achievement-count">
            <span class="number">3</span>
            <span class="label">Neue Meilensteine / New Milestones</span>
        </div>

        <!-- Before/After comparison -->
        <div class="comparison">
            <p class="highlight">
                Vor 4 Wochen konnte {name} noch nicht {milestone}. Jetzt schon! 🎊
            </p>
        </div>

        <!-- Motivational message -->
        <div class="motivational">
            <p>"Du machst das großartig!"</p>
        </div>

        <!-- Link to full progress view -->
        <a href="#" class="view-all-progress">
            Gesamten Fortschritt ansehen / View All Progress
        </a>
    </div>
</div>
```

**Option 2: Weekly Email/Notification** (Future enhancement)
- Store last reminder date
- Check if 7 days passed
- Generate and display/send reminder

**Option 3: Dedicated Progress Page**
- Timeline visualization of all progress
- Chart showing milestone velocity
- Month-by-month breakdown

#### JavaScript for Auto-Refresh
```javascript
// Auto-load progress reminder on dashboard
function loadProgressReminder() {
    fetch('/api/progress-reminder?period=week')
        .then(response => response.json())
        .then(data => {
            displayProgressWidget(data);
        });
}

// Refresh weekly (check on page load)
document.addEventListener('DOMContentLoaded', () => {
    loadProgressReminder();
});
```

#### Translation Keys
```json
{
  "progress_reminder": {
    "title": "Dein Fortschritt / Your Progress",
    "this_week": "Diese Woche / This Week",
    "this_month": "Diesen Monat / This Month",
    "this_quarter": "Letzte 3 Monate / Last 3 Months",
    "achievements": {
      "count": "{count} neue Meilensteine / {count} new milestones",
      "none": "Noch keine neuen Meilensteine diese Woche / No new milestones this week",
      "categories": "Kategorien: {categories}"
    },
    "comparison": {
      "weeks_ago": "Vor {weeks} Wochen / {weeks} weeks ago",
      "couldnt": "{name} konnte noch nicht: / {name} couldn't yet:",
      "now_can": "Jetzt kann {name}: / Now {name} can:",
      "amazing": "Unglaublicher Fortschritt! / Amazing progress!"
    },
    "growth": {
      "weight_gain": "+{kg} kg in {period}",
      "height_gain": "+{cm} cm in {period}"
    },
    "motivational": {
      "random": "Aufmunterung / Encouragement"
    },
    "view_all": "Gesamten Fortschritt ansehen / View All Progress"
  }
}
```

#### Logic for Display
- **Show on dashboard** if there are achievements this week OR significant before/after comparison
- **Auto-refresh** weekly (cache last generated reminder)
- **Personalize** messages with child's name
- **Rotate** motivational messages randomly
- **Highlight** most significant achievement of the period

#### Testing Requirements
- Test with no achievements (graceful empty state)
- Test with various achievement counts
- Test period calculations (week, month, quarter boundaries)
- Test before/after comparisons across different time ranges
- Test growth change calculations
- Test message personalization with child name
- Test both languages
- Test with different corrected ages

---

## Implementation Order & Dependencies

### Recommended Implementation Sequence

1. **Start with 2.5 (Fortschritts-Erinnerungen)**
   - Reason: Builds on existing milestone data, no new data structures needed
   - Low risk, high user impact
   - Can be added to dashboard immediately

2. **Then 2.4 (Beruhigungstechniken & Bindungstipps)**
   - Reason: Static content, no complex logic
   - Parallel work possible (one developer on calming, one on bonding)
   - Provides immediate value to parents

3. **Then 2.1 (Stolz-Archiv)**
   - Reason: Also builds on existing milestone data
   - Requires new UI page but straightforward logic
   - Prepare structure for future photo/video support (Phase 3)

4. **Then 2.3 (Schlafmuster-Tracking)**
   - Reason: First new data structure, but isolated
   - Good learning ground for tracking features
   - Prepares patterns for feeding/crying tracking (Phase 3)

5. **Finally 2.2 (Erweiterte Wachstumskurven)**
   - Reason: Most complex (percentile data, chart library integration)
   - Requires external data source research
   - High visual impact, worth taking time to get right

### Development Timeline Estimate

**Total: ~4-6 weeks for complete Phase 2**

- 2.5 Fortschritts-Erinnerungen: 3-4 days
- 2.4 Beruhigungstechniken & Bindungstipps: 5-6 days (content writing takes time)
- 2.1 Stolz-Archiv: 4-5 days
- 2.3 Schlafmuster-Tracking: 5-6 days
- 2.2 Erweiterte Wachstumskurven: 7-10 days (research + implementation)

Includes time for:
- Testing each feature
- Bilingual content/translations
- Documentation updates
- Integration with existing codebase

---

## Cross-Cutting Concerns

### Data Persistence
All new data (sleep logs) must be stored in `/data/child_data.json`:

```json
{
  "child_name": "...",
  "birth_date": "...",
  "due_date": "...",
  "growth_records": [...],
  "milestone_achievements": [...],
  "sleep_log": [...]  // NEW
}
```

### Translations
Every UI string must exist in both:
- `translations/de.json`
- `translations/en.json`

Follow existing nested structure. Test both languages thoroughly.

### Mobile Responsiveness
Priority for Phase 2:
- All pages must work well on mobile (parents often use phones)
- Touch-friendly buttons and inputs
- Collapsible sections to reduce scrolling
- Fast loading (minimize external dependencies)

### Testing Strategy
For each feature:
1. Unit tests in `test_sensor.py` for backend logic
2. Manual testing of API endpoints (consider Postman collection)
3. Browser testing (Chrome, Firefox, Safari, Mobile browsers)
4. Both language settings
5. Edge cases (empty data, boundary conditions)

### Documentation Updates
After Phase 2:
- Update `CLAUDE.md` with new features
- Update `README.md` with screenshots
- Consider creating `CHANGELOG.md`
- Update config.json if new settings needed

### Git Workflow
- Develop on branch: `claude/phase-2-implementation`
- Create sub-branches for each feature: `claude/phase-2-1-stolz-archiv`, etc.
- Merge each feature to main branch after testing
- Tag releases: `v0.3.0` (Phase 2 complete)

---

## Success Metrics

Phase 2 is successful when:

✅ **All 5 features are implemented and tested**
✅ **Bilingual support is complete** (German and English)
✅ **No regressions** in existing Phase 1 features
✅ **Mobile responsive** on common devices
✅ **Test coverage** for new backend methods
✅ **User documentation** updated
✅ **Code follows existing architecture** (sensor.py logic, run.py API, templates UI)

---

## Future Considerations (Phase 3 Prep)

As we implement Phase 2, keep in mind Phase 3 needs:

1. **File upload infrastructure** (for photos/videos in Stolz-Archiv)
2. **Extended data structures** (for feeding, crying, diaper tracking)
3. **More complex charts** (sleep patterns can be template for other tracking)
4. **Export functionality** (PDF generation for reports)

Design Phase 2 features to be extensible.

---

## Questions & Decisions Needed

### Before Implementation Starts:

1. **Growth Percentile Data Source**: Which standard should we use?
   - Fenton 2013 Preterm Growth Charts (recommended for preemies)
   - WHO Standards
   - Need to research and decide

2. **Chart Library**: Chart.js vs. alternatives?
   - Recommendation: Chart.js (lightweight, well-documented)

3. **Sleep Tracking Depth**: Do we want to track:
   - Just total sleep? (simpler)
   - Or detailed sleep/wake cycles? (more complex but valuable)
   - Recommendation: Start simple (total sleep per session)

4. **Content Sources**: Who will write/review calming & bonding content?
   - Need medical/developmental review
   - Consider partnering with Frühchenwunder e.V.?

5. **Progress Reminder Frequency**: How often to show?
   - Weekly (recommended)
   - Daily (too frequent?)
   - User-configurable (Phase 4?)

---

## Risk Assessment

### Low Risk
- Fortschritts-Erinnerungen (uses existing data)
- Beruhigungstechniken & Bindungstipps (static content)

### Medium Risk
- Stolz-Archiv (new UI page, but straightforward logic)
- Schlafmuster-Tracking (new data structure, but isolated)

### Higher Risk
- Erweiterte Wachstumskurven (external data dependency, complex calculations)
  - Mitigation: Thorough research of percentile data sources
  - Mitigation: Extensive testing of calculations
  - Mitigation: Medical disclaimer prominent

### Overall Risk Level: **Medium**
Phase 2 is well-scoped with manageable complexity. Most features build on existing architecture.

---

## Next Steps

1. **Review this plan** with stakeholders
2. **Answer decision questions** above
3. **Begin implementation** in recommended order
4. **Set up sub-branches** for each feature
5. **Create detailed task breakdown** for first feature (2.5)

---

**Plan created:** 2025-11-09
**Ready for implementation:** Pending decision questions
**Estimated completion:** 4-6 weeks from start
