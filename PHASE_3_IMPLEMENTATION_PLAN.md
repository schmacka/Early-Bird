# Phase 3 Implementation Plan - Erweiterte Features

**Datum:** 2025-11-09
**Status:** Planning
**Basierend auf:** FEATURE_ROADMAP.md Phase 3

---

## Übersicht

Phase 3 implementiert fünf erweiterte Features mit mittlerem Wert und höherem Aufwand:

1. **Foto/Video-Upload zu Meilensteinen** - Media attachments für wichtige Momente
2. **Stuhlgang-Tracking** - Gesundheitsindikator für Verdauung
3. **Fütterungs-Tracking** - Dokumentation von Stillen/Flasche/Beikost
4. **Schreiphasen-Dokumentation** - Tracking von Schreiperioden und Auslösern
5. **Impfkalender** - Erinnerungen an Impftermine basierend auf korrigiertem Alter

---

## 1. Foto/Video-Upload zu Meilensteinen

### Anforderungen

**Funktionale Anforderungen:**
- Upload von Fotos (JPEG, PNG, max 10MB pro Datei)
- Upload von Videos (MP4, MOV, max 50MB pro Datei)
- Mehrere Medien pro Meilenstein (max 5 Dateien)
- Thumbnail-Generierung für Videos
- Verknüpfung mit bestehenden Meilensteinen
- Anzeige in Timeline/Stolz-Archiv

**Nicht-funktionale Anforderungen:**
- Lokale Speicherung (Datenschutz!)
- Lazy Loading für Performance
- Bildoptimierung (automatische Kompression)
- EXIF-Daten-Bereinigung (Datenschutz)

### Datenstruktur

```python
# Erweiterung der bestehenden milestone_achievements Struktur
{
    "milestone_achievements": [
        {
            "timestamp": "2024-11-09T14:30:00",
            "category": "motor",
            "milestone": "Lifts head when on tummy",
            "age_weeks": 8,
            "congratulation": "Großartig! Max macht...",
            "media": [  # NEU
                {
                    "id": "uuid-1234-5678",
                    "type": "image",  # image | video
                    "filename": "first_smile_2024-11-09.jpg",
                    "path": "/data/media/milestones/uuid-1234-5678.jpg",
                    "thumbnail_path": "/data/media/thumbnails/uuid-1234-5678_thumb.jpg",
                    "original_filename": "IMG_1234.jpg",
                    "file_size_bytes": 2457600,
                    "uploaded_at": "2024-11-09T14:35:00",
                    "metadata": {
                        "width": 1920,
                        "height": 1080
                    }
                }
            ]
        }
    ]
}
```

### Storage-Struktur

```
/data/
  ├── child_data.json
  ├── media/
  │   ├── milestones/
  │   │   ├── uuid-1234-5678.jpg
  │   │   ├── uuid-1234-5679.mp4
  │   ├── thumbnails/
  │   │   ├── uuid-1234-5678_thumb.jpg
  │   │   ├── uuid-1234-5679_thumb.jpg
```

### API Endpoints

```python
# POST /api/milestone-achievements/<achievement_id>/media
# Multipart form data upload
Request:
  - file: binary data
  - achievement_id: string (from existing milestone)

Response:
{
    "success": true,
    "media_id": "uuid-1234-5678",
    "thumbnail_url": "/api/media/thumbnails/uuid-1234-5678",
    "file_url": "/api/media/milestones/uuid-1234-5678"
}

# GET /api/media/milestones/<media_id>
# Serve media file with proper MIME type

# GET /api/media/thumbnails/<media_id>
# Serve thumbnail

# DELETE /api/milestone-achievements/<achievement_id>/media/<media_id>
# Remove media file and update achievement
```

### Sensor-Methoden (sensor.py)

```python
def add_media_to_milestone(self, achievement_index, file_data, file_type, original_filename):
    """
    Add media file to milestone achievement

    Args:
        achievement_index: Index of achievement in milestone_achievements list
        file_data: Binary file data
        file_type: 'image' or 'video'
        original_filename: Original filename from upload

    Returns:
        dict: Media metadata with paths
    """

def remove_media_from_milestone(self, achievement_index, media_id):
    """Remove media file and update achievement data"""

def _generate_thumbnail(self, media_path, media_type):
    """Generate thumbnail for image or video"""

def _optimize_image(self, image_path):
    """Compress and optimize image, remove EXIF data"""
```

### UI Komponenten

**Meilenstein-Formular erweitern:**
- Datei-Upload-Button mit Drag & Drop
- Preview von hochgeladenen Medien
- Löschen-Option

**Stolz-Archiv/Timeline:**
- Thumbnail-Grid für Medien
- Lightbox/Modal für Vollansicht
- Video-Player für Video-Dateien

### Technische Anforderungen

**Python Libraries:**
- Pillow (PIL) für Bildverarbeitung
- imageio oder moviepy für Video-Thumbnails
- piexif für EXIF-Daten-Entfernung

**Frontend:**
- FileReader API für Preview
- Drag & Drop Handler
- Video.js oder natives HTML5 Video für Playback

### Sicherheit & Datenschutz

- ✅ Validierung von Dateitypen (MIME-Type + Magic Bytes)
- ✅ Größenbeschränkungen enforced
- ✅ EXIF-Daten entfernen (GPS, Kamera-Metadaten)
- ✅ Speicherplatz-Monitoring (Warnung bei > 80% Speicher)
- ✅ Sanitize Dateinamen (keine Path Traversal)
- ✅ Content-Disposition Header für Downloads

### Testing

```python
def test_add_media_to_milestone():
    # Test successful image upload
    # Test successful video upload
    # Test file size limits
    # Test invalid file types
    # Test EXIF removal
    # Test thumbnail generation

def test_media_storage_limits():
    # Test maximum files per milestone (5)
    # Test total storage warnings
```

---

## 2. Stuhlgang-Tracking

### Anforderungen

**Funktionale Anforderungen:**
- Erfassen von Farbe, Konsistenz, Häufigkeit
- Zeitstempel pro Eintrag
- Warnungen bei ungewöhnlichen Werten
- Trendanzeige über Zeit
- Hinweise: Was ist normal für korrigiertes Alter?

**Disclaimer:**
> ⚠️ Diese Funktion dient nur zur Dokumentation. Bei ungewöhnlichen Farben (rot, schwarz, weiß) oder anhaltenden Auffälligkeiten konsultieren Sie umgehend einen Kinderarzt!

### Datenstruktur

```python
# Neue Struktur in child_data.json
{
    "diaper_logs": [
        {
            "timestamp": "2024-11-09T10:15:00",
            "type": "bowel_movement",  # bowel_movement | wet | both
            "color": "yellow",  # yellow | green | brown | black | red | white
            "consistency": "soft",  # liquid | soft | formed | hard
            "notes": "Nach Stillen, normale Menge",
            "age_weeks_at_log": 8,
            "warnings": []  # Auto-generated based on color/consistency
        }
    ]
}
```

### Referenzdaten (Konstanten)

```python
# In sensor.py
DIAPER_REFERENCE = {
    "normal_colors": {
        "0-1_weeks": ["black", "dark_green"],  # Mekonium
        "1-4_weeks": ["yellow", "green"],  # Muttermilch/Formula
        "4+_weeks": ["yellow", "green", "brown"]
    },
    "warning_colors": ["red", "white", "black"],  # Nach Mekonium-Phase
    "normal_consistency": ["soft", "liquid"],  # Für Stillkinder
    "warning_messages": {
        "red": "Blutbeimengung möglich - SOFORT zum Arzt!",
        "white": "Kann auf Galleprobleme hindeuten - Arzt kontaktieren!",
        "black": "Nach der ersten Woche ungewöhnlich - Arzt konsultieren!"
    }
}
```

### API Endpoints

```python
# POST /api/diaper-logs
Request:
{
    "type": "bowel_movement",
    "color": "yellow",
    "consistency": "soft",
    "notes": "Optional text"
}

Response:
{
    "success": true,
    "log_id": "index-123",
    "warnings": [],
    "normal_for_age": true
}

# GET /api/diaper-logs?days=7
# Get logs from last N days with statistics

Response:
{
    "logs": [...],
    "statistics": {
        "total_count": 15,
        "average_per_day": 2.1,
        "most_common_color": "yellow",
        "warnings_count": 0
    }
}

# GET /api/diaper-logs/reference
# Get age-appropriate reference information
Response:
{
    "current_age_weeks": 8,
    "expected_colors": ["yellow", "green", "brown"],
    "expected_consistency": ["soft", "liquid"],
    "typical_frequency": "2-5 times per day",
    "info": "Stillkinder haben häufig weichen, gelben Stuhl..."
}
```

### Sensor-Methoden

```python
def add_diaper_log(self, log_type, color=None, consistency=None, notes=""):
    """Add diaper change log with automatic warnings"""

def get_diaper_logs(self, days=7):
    """Get recent diaper logs with statistics"""

def _check_diaper_warnings(self, color, consistency, age_weeks):
    """Generate warnings based on color/consistency and age"""

def get_diaper_reference_for_age(self):
    """Get age-appropriate reference information"""
```

### UI Komponenten

**Quick-Log Widget (Dashboard):**
- Große Icons für schnelle Eingabe (Farbe + Konsistenz)
- Zeitstempel automatisch
- Optional: Notiz hinzufügen

**Tracking-Seite:**
- Kalenderansicht mit Häufigkeits-Übersicht
- Farbkodierte Timeline
- Statistiken (Durchschnitt, Trends)
- Warnung-Banner bei kritischen Werten

**Referenz-Info-Box:**
- "Was ist normal für [Name] im Alter von X Wochen?"
- Farbpalette mit Erklärungen

### Testing

```python
def test_diaper_log_warnings():
    # Test warning colors at different ages
    # Test normal vs. warning consistency
    # Test mekonium phase (first week)

def test_diaper_statistics():
    # Test frequency calculations
    # Test trend detection
```

---

## 3. Fütterungs-Tracking

### Anforderungen

**Funktionale Anforderungen:**
- Stillen: Dauer pro Seite, Uhrzeit
- Flasche: Menge in ml, Uhrzeit
- Beikost: Art der Nahrung, Akzeptanz
- Probleme dokumentieren (Andocken, Reflux, etc.)
- Statistiken: Häufigkeit, Abstände, Trends
- Erinnerungen für nächste Fütterung (optional)

### Datenstruktur

```python
{
    "feeding_logs": [
        {
            "timestamp": "2024-11-09T10:00:00",
            "type": "breastfeeding",  # breastfeeding | bottle | solid_food
            "details": {
                # For breastfeeding:
                "left_duration_minutes": 12,
                "right_duration_minutes": 10,

                # For bottle:
                "amount_ml": 120,
                "formula_type": "Pre-Nahrung",

                # For solid food:
                "food_items": ["Karotte", "Kartoffel"],
                "acceptance": "good"  # good | partial | refused
            },
            "problems": {
                "had_problems": false,
                "types": [],  # latching | reflux | gas | refused | other
                "notes": ""
            },
            "age_weeks_at_log": 8
        }
    ]
}
```

### Referenzdaten

```python
FEEDING_REFERENCE = {
    "breastfeeding": {
        "0-4_weeks": {
            "frequency": "8-12 times per day",
            "duration": "10-20 minutes per side",
            "info": "Häufiges Anlegen ist normal und fördert Milchproduktion"
        },
        "4-12_weeks": {
            "frequency": "6-8 times per day",
            "duration": "10-15 minutes per side",
            "info": "Babys werden effizienter beim Trinken"
        }
    },
    "bottle": {
        "0-4_weeks": {
            "amount_ml": "60-90 ml per feeding",
            "frequency": "8-10 times per day"
        },
        "4-8_weeks": {
            "amount_ml": "90-120 ml per feeding",
            "frequency": "6-8 times per day"
        }
    },
    "solid_food_introduction": {
        "recommended_start_weeks": 24,  # Corrected age!
        "signs_of_readiness": [
            "Kann mit Unterstützung sitzen",
            "Zeigt Interesse am Essen",
            "Zungenreflex lässt nach"
        ]
    }
}
```

### API Endpoints

```python
# POST /api/feeding-logs
Request:
{
    "type": "breastfeeding",
    "details": {
        "left_duration_minutes": 12,
        "right_duration_minutes": 10
    },
    "problems": {
        "had_problems": false
    }
}

# GET /api/feeding-logs?hours=24
# Get recent feeding logs

Response:
{
    "logs": [...],
    "statistics": {
        "count_24h": 8,
        "average_interval_hours": 3.2,
        "last_feeding": "2024-11-09T10:00:00",
        "next_feeding_estimate": "2024-11-09T13:12:00"
    }
}

# GET /api/feeding-logs/reference
# Get age-appropriate feeding guidance

# GET /api/feeding-logs/problems-summary?days=7
# Summary of feeding problems in last N days
```

### Sensor-Methoden

```python
def add_feeding_log(self, feeding_type, details, problems=None):
    """Add feeding log entry"""

def get_feeding_logs(self, hours=24):
    """Get recent feeding logs with statistics"""

def get_feeding_statistics(self, days=7):
    """Calculate feeding patterns and trends"""

def estimate_next_feeding(self):
    """Estimate next feeding time based on recent pattern"""

def get_feeding_reference_for_age(self):
    """Get age-appropriate feeding guidance"""

def get_feeding_problems_summary(self, days=7):
    """Analyze feeding problems over time"""
```

### UI Komponenten

**Quick-Log Widget:**
- Große Buttons: Stillen | Flasche | Beikost
- Timer für Stillen (Start/Stop pro Seite)
- Menge-Eingabe für Flasche
- Optional: Probleme markieren

**Tracking-Dashboard:**
- Zeitachse der letzten 24h
- Intervall-Visualisierung
- Statistiken-Cards (Anzahl, Durchschnitt, Nächste Fütterung)
- Problem-Trend-Chart

**Referenz-Info:**
- "Was ist normal für [Name]?"
- Beikost-Bereitschafts-Check (ab ~24 Wochen)

### Testing

```python
def test_feeding_log_types():
    # Test breastfeeding log
    # Test bottle log
    # Test solid food log

def test_feeding_statistics():
    # Test interval calculations
    # Test next feeding estimation
    # Test problem trend analysis
```

---

## 4. Schreiphasen-Dokumentation

### Anforderungen

**Funktionale Anforderungen:**
- Dauer der Schreiepisode erfassen
- Intensität bewerten (1-5 Sterne)
- Mögliche Auslöser notieren
- Was hat geholfen? (Techniken)
- Korrelation mit Wonder Weeks zeigen
- Trend-Analyse: Besser/schlechter werdend?

**Ziel:** Eltern helfen, Muster zu erkennen und Strategien zu finden

### Datenstruktur

```python
{
    "crying_logs": [
        {
            "start_time": "2024-11-09T19:00:00",
            "end_time": "2024-11-09T19:45:00",
            "duration_minutes": 45,
            "intensity": 4,  # 1-5 scale
            "possible_triggers": [
                "tired",
                "overstimulated",
                "hungry",
                "diaper",
                "unknown"
            ],
            "what_helped": [
                "white_noise",
                "rocking",
                "feeding",
                "skin_to_skin",
                "nothing"
            ],
            "notes": "Abends nach vielen Besuchern",
            "age_weeks_at_log": 8,
            "wonder_week_active": true,
            "wonder_week_name": "Patterns"
        }
    ]
}
```

### Referenzdaten

```python
CRYING_REFERENCE = {
    "typical_patterns": {
        "0-6_weeks": {
            "peak_hours": ["18:00-22:00"],
            "info": "Abendliche Unruhe ('Hexenstunde') ist normal",
            "average_daily_minutes": "120-180"
        },
        "6-12_weeks": {
            "peak_hours": ["18:00-21:00"],
            "info": "Crying often peaks around 6 weeks, then decreases",
            "average_daily_minutes": "90-150"
        }
    },
    "common_triggers": [
        {"id": "tired", "name": "Müdigkeit"},
        {"id": "hungry", "name": "Hunger"},
        {"id": "overstimulated", "name": "Überstimulation"},
        {"id": "diaper", "name": "Volle Windel"},
        {"id": "gas", "name": "Bauchschmerzen/Blähungen"},
        {"id": "wonder_week", "name": "Entwicklungssprung"},
        {"id": "unknown", "name": "Unbekannt"}
    ],
    "soothing_techniques": [
        {"id": "white_noise", "name": "Weißes Rauschen"},
        {"id": "rocking", "name": "Wiegen/Schaukeln"},
        {"id": "swaddle", "name": "Pucken"},
        {"id": "feeding", "name": "Füttern"},
        {"id": "skin_to_skin", "name": "Körperkontakt"},
        {"id": "pacifier", "name": "Schnuller"},
        {"id": "carrying", "name": "Tragen"},
        {"id": "change_environment", "name": "Umgebungswechsel"},
        {"id": "nothing", "name": "Nichts half"}
    ]
}
```

### API Endpoints

```python
# POST /api/crying-logs
Request:
{
    "start_time": "2024-11-09T19:00:00",
    "end_time": "2024-11-09T19:45:00",
    "intensity": 4,
    "possible_triggers": ["tired", "overstimulated"],
    "what_helped": ["white_noise", "rocking"],
    "notes": "Optional"
}

# GET /api/crying-logs?days=7
Response:
{
    "logs": [...],
    "statistics": {
        "total_episodes": 12,
        "total_minutes": 340,
        "average_duration_minutes": 28,
        "average_intensity": 3.2,
        "peak_hours": ["19:00", "20:00"],
        "most_common_triggers": ["tired", "wonder_week"],
        "most_effective_techniques": ["white_noise", "rocking"]
    },
    "wonder_week_correlation": {
        "in_wonder_week": true,
        "episodes_during_leaps": 8,
        "episodes_outside_leaps": 4
    }
}

# GET /api/crying-logs/patterns
# Analyze patterns over longer period (30 days)

# GET /api/crying-logs/reference
# Get age-appropriate reference info
```

### Sensor-Methoden

```python
def add_crying_log(self, start_time, end_time, intensity, triggers, helped, notes=""):
    """Add crying episode with Wonder Week correlation"""

def get_crying_logs(self, days=7):
    """Get recent crying logs with statistics"""

def analyze_crying_patterns(self, days=30):
    """Analyze long-term patterns and trends"""

def get_crying_wonder_week_correlation(self):
    """Check correlation between crying and Wonder Weeks"""

def get_crying_reference_for_age(self):
    """Get age-appropriate crying info"""
```

### UI Komponenten

**Quick-Log:**
- Start/Stop Timer für Episode
- Quick-Intensity-Slider (1-5)
- Multi-Select für Trigger und Hilfen
- Notiz-Feld

**Analyse-Dashboard:**
- Zeitachse mit Episoden
- Heatmap für Tageszeiten
- Wonder Week Overlay
- "Was hilft am besten?" - Ranking
- Trend: Besser/schlechter werdend

**Ermutigung:**
- Positive Messages: "Du machst das großartig!"
- Hinweis auf Wonder Week-Zusammenhang
- Erinnerung: "Das geht vorbei"

### Testing

```python
def test_crying_log_statistics():
    # Test duration calculations
    # Test peak hour detection
    # Test effectiveness ranking

def test_wonder_week_correlation():
    # Test correlation detection
    # Test with/without leap episodes
```

---

## 5. Impfkalender

### Anforderungen

**Funktionale Anforderungen:**
- Standard-Impfplan basierend auf korrigiertem Alter
- Anpassbare Termine (individuelle Verschiebungen)
- Abhaken erledigter Impfungen
- Erinnerungen X Tage vor Termin
- Historie aller Impfungen
- Charge/Lot-Nummer optional erfassen
- Nächste anstehende Impfung anzeigen

**Wichtig:**
- STIKO-Empfehlungen für Deutschland
- Hinweis: Angepasst für korrigiertes Alter!
- Disclaimer: Mit Kinderarzt absprechen

### Datenstruktur

```python
# Impfplan als Konstante (STIKO-konform)
VACCINATION_SCHEDULE = [
    {
        "name": "6-fach-Impfung (DTaP-IPV-Hib-HepB)",
        "description": "Diphtherie, Tetanus, Pertussis, Polio, Hib, Hepatitis B",
        "doses": [
            {"dose_number": 1, "age_weeks": 8},
            {"dose_number": 2, "age_weeks": 12},
            {"dose_number": 3, "age_weeks": 16},
            {"dose_number": 4, "age_weeks": 52}  # Booster
        ],
        "info": "Grundimmunisierung erfolgt in 3 Dosen"
    },
    {
        "name": "Pneumokokken",
        "doses": [
            {"dose_number": 1, "age_weeks": 8},
            {"dose_number": 2, "age_weeks": 16},
            {"dose_number": 3, "age_weeks": 52}
        ]
    },
    {
        "name": "Rotavirus",
        "doses": [
            {"dose_number": 1, "age_weeks": 8},
            {"dose_number": 2, "age_weeks": 12},
            {"dose_number": 3, "age_weeks": 16}
        ],
        "info": "Schluckimpfung, sollte bis spätestens 24. Woche abgeschlossen sein"
    },
    {
        "name": "MMR (Masern, Mumps, Röteln)",
        "doses": [
            {"dose_number": 1, "age_weeks": 52},
            {"dose_number": 2, "age_weeks": 78}
        ]
    },
    {
        "name": "Varizellen (Windpocken)",
        "doses": [
            {"dose_number": 1, "age_weeks": 52},
            {"dose_number": 2, "age_weeks": 78}
        ]
    }
]

# Tatsächliche Impfungen
{
    "vaccinations": [
        {
            "vaccine_name": "6-fach-Impfung (DTaP-IPV-Hib-HepB)",
            "dose_number": 1,
            "scheduled_date": "2024-11-15",
            "scheduled_age_weeks": 8,
            "completed": true,
            "completed_date": "2024-11-15",
            "location": "Dr. Müller, Kinderarzt",
            "lot_number": "ABC123",  # Optional
            "notes": "Gut vertragen, keine Nebenwirkungen",
            "reminder_sent": true,
            "reminder_days_before": 7
        }
    ]
}
```

### API Endpoints

```python
# GET /api/vaccinations/schedule
# Get full vaccination schedule with status
Response:
{
    "schedule": [
        {
            "vaccine_name": "6-fach-Impfung",
            "doses": [
                {
                    "dose_number": 1,
                    "recommended_age_weeks": 8,
                    "scheduled_date": "2024-11-15",
                    "completed": true,
                    "completed_date": "2024-11-15",
                    "overdue": false
                },
                {
                    "dose_number": 2,
                    "recommended_age_weeks": 12,
                    "scheduled_date": null,
                    "completed": false,
                    "overdue": false,
                    "due_in_days": 14
                }
            ]
        }
    ],
    "next_vaccination": {
        "vaccine_name": "6-fach-Impfung",
        "dose_number": 2,
        "scheduled_date": "2024-11-29",
        "days_until": 14
    }
}

# POST /api/vaccinations
# Schedule or record vaccination
Request:
{
    "vaccine_name": "6-fach-Impfung",
    "dose_number": 1,
    "scheduled_date": "2024-11-15",
    "reminder_days_before": 7
}

# PUT /api/vaccinations/<vaccination_id>
# Mark as completed
Request:
{
    "completed": true,
    "completed_date": "2024-11-15",
    "location": "Dr. Müller",
    "lot_number": "ABC123",
    "notes": "Gut vertragen"
}

# GET /api/vaccinations/upcoming?weeks=8
# Get vaccinations due in next N weeks

# GET /api/vaccinations/history
# Get all completed vaccinations
```

### Sensor-Methoden

```python
def get_vaccination_schedule(self):
    """
    Get complete vaccination schedule with status
    Calculates recommended dates based on corrected age
    """

def schedule_vaccination(self, vaccine_name, dose_number, scheduled_date, reminder_days=7):
    """Schedule a vaccination"""

def complete_vaccination(self, vaccination_id, completed_date, location=None, lot_number=None, notes=""):
    """Mark vaccination as completed"""

def get_upcoming_vaccinations(self, weeks=8):
    """Get vaccinations due in next N weeks"""

def get_vaccination_history(self):
    """Get all completed vaccinations"""

def check_overdue_vaccinations(self):
    """Check for overdue vaccinations"""

def get_next_vaccination(self):
    """Get next scheduled/due vaccination"""
```

### UI Komponenten

**Impfkalender-Übersicht:**
- Timeline-Ansicht mit allen Impfungen
- Status-Badges: Geplant | Erledigt | Überfällig
- Farbkodierung nach Impfstoff
- Nächste Impfung prominent hervorgehoben

**Impfung-Detail-Card:**
- Name, Dosis, Datum
- Abhaken-Checkbox
- Optionale Felder: Ort, Lot-Nr., Notizen
- Info-Button mit Erklärung zur Impfung

**Erinnerungs-System:**
- Dashboard-Badge: "Impfung in X Tagen"
- Optional: Benachrichtigung in Home Assistant

**Historie:**
- Liste aller erledigten Impfungen
- Export als PDF (für Arztbesuche)

### Integration mit Home Assistant

```yaml
# Sensor für nächste Impfung
sensor:
  - platform: early_bird
    name: "Next Vaccination"
    value_template: "{{ state_attr('sensor.early_bird', 'next_vaccination_name') }}"

# Automation für Erinnerung
automation:
  - alias: "Vaccination Reminder"
    trigger:
      platform: template
      value_template: "{{ state_attr('sensor.early_bird', 'next_vaccination_days') <= 7 }}"
    action:
      service: notify.mobile_app
      data:
        title: "Impftermin für {{ child_name }}"
        message: "Impfung in {{ days }} Tagen!"
```

### Testing

```python
def test_vaccination_schedule_generation():
    # Test schedule based on corrected age
    # Test premature baby (schedule shifts)

def test_vaccination_reminders():
    # Test reminder triggers
    # Test overdue detection

def test_vaccination_completion():
    # Test marking as complete
    # Test history retrieval
```

---

## Gemeinsame Technische Anforderungen

### 1. Datenmigration

Beim Update von Phase 2 zu Phase 3 müssen bestehende `child_data.json` Dateien erweitert werden:

```python
def migrate_data_to_phase3(data):
    """
    Migrate existing data structure to Phase 3 format
    Adds new empty arrays for new features
    """
    if "diaper_logs" not in data:
        data["diaper_logs"] = []
    if "feeding_logs" not in data:
        data["feeding_logs"] = []
    if "crying_logs" not in data:
        data["crying_logs"] = []
    if "vaccinations" not in data:
        data["vaccinations"] = []

    # Extend milestone_achievements with media array
    for achievement in data.get("milestone_achievements", []):
        if "media" not in achievement:
            achievement["media"] = []

    return data
```

### 2. Storage Management

**Speicherplatz-Monitoring:**

```python
def check_storage_usage(self):
    """
    Check disk usage for /data volume
    Return warning if > 80% full
    """
    total, used, free = shutil.disk_usage("/data")
    percent_used = (used / total) * 100

    return {
        "total_gb": total / (1024**3),
        "used_gb": used / (1024**3),
        "free_gb": free / (1024**3),
        "percent_used": percent_used,
        "warning": percent_used > 80
    }

# Add to /api/summary endpoint
```

**Media Cleanup:**

```python
def cleanup_orphaned_media(self):
    """
    Remove media files that are no longer referenced
    in milestone_achievements
    """
```

### 3. Translation Files

Alle neuen Features benötigen Übersetzungen in `de.json` und `en.json`:

```json
{
    "diaper_tracking": {
        "title": "Windel-Tracking",
        "color": "Farbe",
        "consistency": "Konsistenz",
        "colors": {
            "yellow": "Gelb",
            "green": "Grün",
            "brown": "Braun",
            "black": "Schwarz",
            "red": "Rot",
            "white": "Weiß"
        },
        "warnings": {
            "red": "Blutbeimengung möglich - SOFORT zum Arzt!",
            "white": "Kann auf Galleprobleme hindeuten - Arzt kontaktieren!"
        }
    },
    "feeding_tracking": { /* ... */ },
    "crying_tracking": { /* ... */ },
    "vaccinations": { /* ... */ }
}
```

### 4. Performance-Optimierungen

**Lazy Loading:**
- Medien-Dateien nur laden bei Bedarf
- Thumbnails für Vorschau nutzen
- Pagination für lange Listen (z.B. Feeding-Logs)

**Caching:**
- Vaccination Schedule (ändert sich selten)
- Reference Data (DIAPER_REFERENCE, etc.)
- Media Thumbnails

**Datenbank-Indizes:**
- Zeitstempel-basierte Queries optimieren
- Eventuell Wechsel von JSON zu SQLite für bessere Performance bei vielen Logs

### 5. Sicherheit

**Input Validation:**
```python
def validate_diaper_log(data):
    allowed_colors = ["yellow", "green", "brown", "black", "red", "white"]
    allowed_consistency = ["liquid", "soft", "formed", "hard"]

    if data.get("color") not in allowed_colors:
        raise ValueError("Invalid color")
    if data.get("consistency") not in allowed_consistency:
        raise ValueError("Invalid consistency")
```

**File Upload Security:**
- MIME-Type validation
- Magic Bytes checking (erste Bytes der Datei prüfen)
- Path Traversal Prevention
- Maximum file size enforcement
- Virus scanning (optional, falls verfügbar)

**CSRF Protection:**
- Token-basierte API-Aufrufe für state-changing operations

### 6. Error Handling

Alle neuen Endpoints brauchen einheitliches Error Handling:

```python
@app.route('/api/diaper-logs', methods=['POST'])
def api_diaper_logs_post():
    try:
        data = request.json
        validate_diaper_log(data)
        result = sensor.add_diaper_log(...)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error adding diaper log: {e}")
        return jsonify({"error": "Internal server error"}), 500
```

---

## Implementierungs-Reihenfolge

### Priorität 1 - Grundlagen (Woche 1-2)

1. **Datenmigration implementieren**
   - Migration-Script für bestehende Daten
   - Tests für Migration

2. **Impfkalender** (hoher Wert, klar definiert)
   - VACCINATION_SCHEDULE Konstante
   - API-Endpoints
   - Sensor-Methoden
   - Einfache UI (Tabelle)
   - Translations

### Priorität 2 - Tracking-Features (Woche 3-4)

3. **Fütterungs-Tracking**
   - Datenstruktur
   - API-Endpoints
   - Sensor-Methoden
   - Quick-Log UI
   - Statistics-Dashboard

4. **Stuhlgang-Tracking**
   - Datenstruktur + Referenzdaten
   - Warning-System
   - API-Endpoints
   - UI mit Farbauswahl

### Priorität 3 - Erweiterte Features (Woche 5-6)

5. **Schreiphasen-Dokumentation**
   - Datenstruktur
   - Wonder Week Correlation
   - Pattern-Analysis
   - UI mit Timer

### Priorität 4 - Media Upload (Woche 7-8)

6. **Foto/Video-Upload**
   - File Upload Handler
   - Storage Management
   - Thumbnail Generation
   - Integration in Meilensteine
   - UI-Komponenten

**Begründung für diese Reihenfolge:**
- Impfkalender ist am klarsten definiert und hat hohen Wert
- Tracking-Features bauen aufeinander auf (ähnliche Patterns)
- Media-Upload ist am komplexesten → zuletzt, wenn Patterns klar sind

---

## Testing-Strategie

### Unit Tests

Für jedes Feature:
```python
# test_phase3_features.py

class TestDiaperTracking(unittest.TestCase):
    def test_add_diaper_log(self):
    def test_diaper_warnings(self):
    def test_age_appropriate_reference(self):

class TestFeedingTracking(unittest.TestCase):
    def test_add_feeding_log_breastfeeding(self):
    def test_add_feeding_log_bottle(self):
    def test_feeding_statistics(self):
    def test_next_feeding_estimate(self):

class TestCryingTracking(unittest.TestCase):
    def test_add_crying_log(self):
    def test_wonder_week_correlation(self):
    def test_pattern_analysis(self):

class TestVaccinations(unittest.TestCase):
    def test_schedule_generation(self):
    def test_overdue_detection(self):
    def test_complete_vaccination(self):

class TestMediaUpload(unittest.TestCase):
    def test_image_upload(self):
    def test_video_upload(self):
    def test_file_validation(self):
    def test_thumbnail_generation(self):
    def test_storage_limits(self):
```

### Integration Tests

```python
def test_full_workflow_feeding_to_diaper():
    # Test realistic scenario: Feeding → Diaper log

def test_crying_with_wonder_week_context():
    # Test crying log during active wonder week

def test_milestone_with_media_upload():
    # Test complete flow: milestone → photo upload → display
```

### Performance Tests

```python
def test_large_dataset_performance():
    # Test with 1000+ feeding logs
    # Test with 500+ diaper logs
    # Ensure API response < 200ms

def test_media_storage_performance():
    # Test with 100+ media files
    # Test thumbnail loading
```

---

## Dokumentation-Updates

### CLAUDE.md Update

```markdown
## Phase 3 Features (NEW)

### Tracking Features
- Diaper Tracking: Color, consistency with age-appropriate warnings
- Feeding Tracking: Breastfeeding, bottle, solid food
- Crying Logs: Duration, triggers, Wonder Week correlation

### Media Upload
- Photos/videos can be attached to milestones
- Stored locally in /data/media/
- Automatic thumbnail generation

### Vaccination Calendar
- STIKO-compliant schedule based on corrected age
- Reminders and completion tracking
- Export for doctor visits

### Data Structure Updates
```json
{
    "milestone_achievements": [...],  // Extended with media array
    "diaper_logs": [...],
    "feeding_logs": [...],
    "crying_logs": [...],
    "vaccinations": [...]
}
```
```

### API Documentation

Neue API-Dokumentations-Datei: `API.md`

```markdown
# Early Bird API Documentation

## Phase 3 Endpoints

### Diaper Tracking
- POST /api/diaper-logs
- GET /api/diaper-logs?days=7
- GET /api/diaper-logs/reference

[Detailed specs...]

### Feeding Tracking
[...]

### Crying Tracking
[...]

### Vaccinations
[...]

### Media Upload
[...]
```

---

## Risiken & Mitigation

### Risiko 1: Speicherplatz

**Problem:** Media-Uploads können schnell Speicher füllen

**Mitigation:**
- Strikte Dateigrößen-Limits (10MB Images, 50MB Videos)
- Automatische Bildkompression
- Storage-Monitoring mit Warnings
- Optional: Cleanup alter Medien nach X Monaten

### Risiko 2: Performance bei vielen Logs

**Problem:** Tausende Feeding/Diaper-Logs verlangsamen API

**Mitigation:**
- Pagination implementieren
- Indizes in JSON oder Migration zu SQLite
- Lazy Loading in UI
- Aggregierte Statistiken cachen

### Risiko 3: Datenschutz bei Media

**Problem:** Fotos können sensible Metadaten enthalten

**Mitigation:**
- EXIF-Daten automatisch entfernen
- Lokale Speicherung (keine Cloud)
- Clear Documentation über Datenspeicherung
- Optional: Encryption at rest

### Risiko 4: Komplexität für Nutzer

**Problem:** Zu viele Tracking-Optionen können überfordern

**Mitigation:**
- Alle Features optional/abschaltbar
- Quick-Log Widgets für einfache Eingabe
- Progressive Disclosure (Basis → Erweitert)
- Gute Onboarding-Texte

---

## Erfolgs-Metriken

Nach Phase 3 Implementierung sollte folgendes messbar sein:

1. **Feature Adoption:**
   - % der Nutzer, die Feeding-Tracking nutzen
   - % der Nutzer, die Media-Uploads nutzen
   - Durchschn. Anzahl Logs pro Nutzer/Woche

2. **Performance:**
   - API Response Times < 200ms
   - Media Upload Success Rate > 95%
   - Storage Usage im Rahmen

3. **Code Quality:**
   - Test Coverage > 80%
   - Keine kritischen Bugs nach 2 Wochen
   - Alle Features dokumentiert

---

## Nächste Schritte

1. **Review dieses Plans mit Stakeholdern**
   - Feedback einholen
   - Priorisierung bestätigen

2. **Environment Setup**
   - Dependencies installieren (Pillow, imageio)
   - Test-Environment aufsetzen

3. **Implementierung starten**
   - Branch: `feature/phase-3`
   - Start mit Impfkalender
   - Feature-für-Feature mit Testing

4. **Kontinuierliches Review**
   - Nach jedem Feature: Code Review
   - UX-Testing mit echten Eltern
   - Performance-Monitoring

---

**Geschätzte Gesamtdauer:** 8 Wochen
**Erforderliche Skills:** Python, Flask, File Handling, Frontend (HTML/JS)
**Dependencies:** Pillow, imageio, dateutil (bereits vorhanden)

**Letztes Update:** 2025-11-09
