# Early Bird Documentation

## Overview

Early Bird is a Home Assistant addon designed for tracking the development of premature children. It provides corrected age calculations, milestone tracking, and Wonder Weeks integration specifically adjusted for premature babies.

## Installation

1. Navigate to your Home Assistant instance
2. Go to Supervisor → Add-on Store
3. Add this repository URL (if not already added)
4. Find "Early Bird" in the add-on list
5. Click "Install"
6. Wait for the installation to complete

## Configuration

Before starting the addon, you must configure the following required fields:

### Required Configuration

- **birth_date**: The actual birth date of your child (format: YYYY-MM-DD)
- **due_date**: The originally calculated due date (format: YYYY-MM-DD)

Example:
```json
{
  "child_name": "Emma",
  "birth_date": "2024-01-15",
  "due_date": "2024-03-01",
  "language": "de",
  "notifications_enabled": true
}
```

### Configuration Options

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| child_name | string | No | "Baby" | Name of your child |
| birth_date | string | Yes | - | Actual birth date (YYYY-MM-DD) |
| due_date | string | Yes | - | Original due date (YYYY-MM-DD) |
| language | list | No | "de" | Interface language (de or en) |
| notifications_enabled | boolean | No | true | Enable Home Assistant notifications |

## Starting the Addon

1. After configuring, click "Start"
2. Wait for the addon to initialize
3. Access the web interface at: `http://homeassistant.local:8099`
   - Or use your Home Assistant IP: `http://YOUR_HA_IP:8099`

## Using the Dashboard

### Age Display

The dashboard shows three types of age:

1. **Corrected Age**: How old your baby would be if born on the due date
2. **Actual Age**: How old your baby is since birth
3. **Prematurity**: How early your baby was born

This helps you understand developmental expectations based on corrected age rather than actual age.

### Wonder Weeks

Based on the book "Oje, Ich Wachse!" (The Wonder Weeks), the addon tracks 10 major developmental leaps:

1. Week 5: Changing Sensations
2. Week 8: Patterns
3. Week 12: Smooth Transitions
4. Week 19: Events
5. Week 26: Relationships
6. Week 37: Categories
7. Week 46: Sequences
8. Week 55: Programs
9. Week 64: Principles
10. Week 75: Systems

All leap timing is based on corrected age, not actual age.

### Milestone Tracking

The addon tracks three categories of milestones:

- **Motor Skills**: Physical development (rolling, sitting, crawling, walking)
- **Cognitive Development**: Mental development (recognition, problem-solving)
- **Language Development**: Communication skills (cooing, babbling, first words)

Milestones are presented based on corrected age.

### Recording Growth

You can record:
- Weight (kg)
- Height (cm)
- Head circumference (cm) - optional

All measurements are stored with both corrected and actual age for accurate tracking.

### Recording Milestone Achievements

When your child achieves a milestone:
1. Select the category (Motor, Cognitive, or Language)
2. Describe the milestone
3. Click "Save"

The achievement is recorded with the current corrected age.

## Data Storage

All data is stored locally in your Home Assistant instance at `/addon_configs/early_bird/child_data.json`. This includes:
- Growth measurements
- Milestone achievements
- Historical records

Your data never leaves your Home Assistant instance.

## API Endpoints

The addon provides a REST API for integration with Home Assistant automations:

### GET /api/summary
Get complete summary of all data.

### GET /api/age
Get current corrected and actual age information.

Response example:
```json
{
  "corrected_age": {
    "years": 0,
    "months": 3,
    "weeks": 2,
    "days": 1,
    "total_weeks": 14,
    "total_days": 98
  },
  "actual_age": {
    "years": 0,
    "months": 5,
    "weeks": 0,
    "days": 1
  },
  "prematurity": {
    "weeks": 8,
    "days": 0,
    "total_days": 56
  }
}
```

### GET /api/wonder-weeks
Get current Wonder Week information.

### GET /api/milestones
Get upcoming milestones.

Query parameters:
- `category` (optional): Filter by category (motor, cognitive, language)
- `weeks_ahead` (optional, default 12): How many weeks to look ahead

### POST /api/growth
Add a growth measurement.

Body:
```json
{
  "weight_kg": 4.5,
  "height_cm": 52.0,
  "head_circumference_cm": 38.0
}
```

### POST /api/milestone-achievements
Record a milestone achievement.

Body:
```json
{
  "category": "motor",
  "milestone": "First smile"
}
```

## Home Assistant Integration

### Creating Sensors

You can create template sensors in Home Assistant to display the data:

```yaml
sensor:
  - platform: rest
    name: Baby Corrected Age
    resource: http://localhost:8099/api/age
    value_template: "{{ value_json.corrected_age.total_weeks }}"
    unit_of_measurement: "weeks"
    scan_interval: 3600

  - platform: rest
    name: Baby Wonder Week
    resource: http://localhost:8099/api/wonder-weeks
    value_template: "{{ value_json.current_week }}"
    scan_interval: 3600
```

### Creating Automations

Example automation to notify about Wonder Weeks:

```yaml
automation:
  - alias: "Wonder Week Notification"
    trigger:
      - platform: state
        entity_id: sensor.baby_wonder_week
    action:
      - service: notify.mobile_app
        data:
          title: "Wonder Week Update"
          message: "Baby is now in week {{ states('sensor.baby_wonder_week') }}"
```

## Understanding Corrected Age

Corrected age (also called adjusted age) is crucial for premature babies:

- **Use corrected age** for tracking development milestones
- **Use corrected age** for comparing with growth charts
- **Use corrected age** for Wonder Weeks tracking
- Most pediatricians use corrected age until age 2-3

### Example

- Birth: January 1, 2024
- Due date: March 1, 2024
- Prematurity: 8 weeks

On April 1, 2024:
- **Actual age**: 13 weeks (3 months from birth)
- **Corrected age**: 5 weeks (5 weeks from due date)

Use corrected age (5 weeks) for development expectations.

## Troubleshooting

### Addon won't start
- Check that birth_date and due_date are configured
- Verify date format is YYYY-MM-DD
- Check addon logs in Home Assistant

### Can't access web interface
- Verify the addon is running
- Try accessing via IP: `http://YOUR_HA_IP:8099`
- Check if port 8099 is available

### Data not saving
- Check Home Assistant has write permissions to addon data directory
- Review addon logs for errors

## Privacy & Security

- All data is stored locally in Home Assistant
- No external services or cloud connections
- Data never leaves your network
- AppArmor security profile included

## Support

For issues or questions:
1. Check the logs in Home Assistant Supervisor
2. Review this documentation
3. Open an issue on GitHub

## References

- "The Wonder Weeks" by Frans X. Plooij and Hetty van de Rijt
- "Oje, Ich Wachse!" (German edition)
- WHO Growth Standards for premature infants
- AAP Guidelines for premature infant development

## Disclaimer

This addon is for informational purposes only. Always consult with your pediatrician regarding your child's development and health. The information provided should not replace professional medical advice.
