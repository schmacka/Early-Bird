# Early Bird - Home Assistant Addon

Track the development of premature children with corrected age calculations, milestone tracking, and Wonder Weeks integration.

## Features

- 📅 **Corrected Age Calculator**: Automatically calculates corrected age based on due date vs actual birth date
- 🌟 **Wonder Weeks Integration**: Track developmental leaps adjusted for corrected age based on "Oje, Ich Wachse!" (The Wonder Weeks)
- 🎯 **Milestone Tracking**: Monitor motor, cognitive, and language development milestones
- 📊 **Growth Monitoring**: Track weight, height, and head circumference over time
- 💾 **Local Data Storage**: All data stored locally in Home Assistant
- 🔔 **Home Assistant Notifications**: Get notified about upcoming developmental leaps
- 🇩🇪 **German Language Support**: Fully translated interface

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "Early Bird" addon
3. Configure the addon with your child's information (see Configuration section)
4. Start the addon
5. Access the web interface at `http://homeassistant:8099`

## Configuration

The addon requires the following configuration:

### Required Settings

- **birth_date**: Your child's actual birth date in format YYYY-MM-DD (e.g., "2024-01-15")
- **due_date**: The originally calculated due date in format YYYY-MM-DD (e.g., "2024-03-01")

### Optional Settings

- **child_name**: Your child's name (default: "Baby")
- **language**: Interface language - "de" for German or "en" for English (default: "de")
- **notifications_enabled**: Enable/disable Home Assistant notifications (default: true)

### Example Configuration

```json
{
  "child_name": "Emma",
  "birth_date": "2024-01-15",
  "due_date": "2024-03-01",
  "language": "de",
  "notifications_enabled": true
}
```

## Using the Dashboard

The Early Bird dashboard provides several features:

### Age Display
- Shows both corrected age (based on due date) and actual age (from birth)
- Displays how premature your child was born
- Updates automatically

### Wonder Weeks
- Shows current or upcoming developmental leap
- Based on the "Oje, Ich Wachse!" leap theory
- Adjusted for your child's corrected age

### Upcoming Milestones
- Displays next developmental milestones in motor skills, cognitive development, and language
- Shows when each milestone is expected
- Based on corrected age

### Growth Tracking
- Record weight (kg), height (cm), and optional head circumference (cm)
- Track growth over time
- All measurements stored locally

### Milestone Recording
- Record when your child achieves milestones
- Categorize by motor, cognitive, or language development
- Keep a historical record of achievements

## API Endpoints

The addon provides a REST API for integration:

- `GET /api/summary` - Complete summary of all data
- `GET /api/age` - Current corrected and actual age
- `GET /api/wonder-weeks` - Current Wonder Week information
- `GET /api/milestones` - Upcoming milestones (optional params: category, weeks_ahead)
- `GET /api/growth` - Get all growth records
- `POST /api/growth` - Add a growth record
- `GET /api/milestone-achievements` - Get all recorded achievements
- `POST /api/milestone-achievements` - Record a milestone achievement
- `GET /health` - Health check endpoint

## Data Storage

All data is stored locally in `/data/child_data.json` and persists across addon restarts.

## Wonder Weeks Reference

The addon tracks the following developmental leaps:

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

All weeks are calculated based on the corrected age (from due date), making it perfect for premature babies.

## Understanding Corrected Age

Corrected age is crucial for premature babies. It represents how old your baby would be if they had been born on their due date. For example:

- Birth date: January 15, 2024
- Due date: March 1, 2024
- Prematurity: 6 weeks 4 days

On April 1, 2024:
- Actual age: 11 weeks 4 days
- Corrected age: 4 weeks 3 days

Use corrected age when:
- Tracking developmental milestones
- Comparing with growth charts
- Assessing Wonder Weeks leaps

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

## License

This addon is provided as-is for personal use.

## Disclaimer

This addon is for informational purposes only and should not replace professional medical advice. Always consult with your pediatrician regarding your child's development.
