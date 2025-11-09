# Early Bird - Home Assistant Addon

🐣 Track the development of premature children with corrected age calculations, milestone tracking, and Wonder Weeks integration.

## Overview

Early Bird is a Home Assistant addon designed specifically for parents of premature babies. It helps track development using corrected age calculations, ensuring that milestones and developmental leaps are properly adjusted for prematurity.

## Key Features

- **Corrected Age Calculator**: Automatically calculates corrected age based on due date vs actual birth date
- **Wonder Weeks Integration**: Track developmental leaps based on "Oje, Ich Wachse!" (The Wonder Weeks), adjusted for corrected age
- **Milestone Tracking**: Monitor motor, cognitive, and language development milestones
- **Growth Monitoring**: Track weight, height, and head circumference with historical records
- **Local Data Storage**: All data stored securely in your Home Assistant instance
- **Home Assistant Notifications**: Get notified about upcoming developmental leaps
- **German & English Support**: Fully translated user interface

## Quick Start

1. Install the addon from the Home Assistant addon store
2. Configure with your child's birth date and due date
3. Access the dashboard to start tracking development
4. Record growth measurements and milestone achievements

## Documentation

Full documentation is available in the [addon README](early_bird/README.md).

## What is Corrected Age?

Corrected age (also called adjusted age) is how old your baby would be if they had been born on their due date. This is crucial for premature babies because:

- Developmental milestones should be tracked against corrected age, not actual age
- Growth charts are more accurate when using corrected age
- Wonder Weeks leaps occur based on brain development, which follows corrected age

For example, a baby born 8 weeks early who is 12 weeks old has a corrected age of only 4 weeks.

## Technology Stack

- **Backend**: Python 3 with Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Container**: Docker (Alpine Linux)
- **Storage**: JSON file-based local storage

## Repository Structure

```
/early_bird/            # Main addon directory
  ├── config.json       # Addon manifest and schema
  ├── Dockerfile        # Container configuration
  ├── requirements.txt  # Python dependencies
  ├── run.py           # Flask application
  ├── sensor.py        # Core logic for calculations
  ├── templates/       # HTML templates
  ├── translations/    # Language files
  └── README.md        # Detailed documentation
```

## Support

For issues, questions, or feature requests, please open an issue on this repository.

## License

This project is provided as-is for personal use.

## Disclaimer

This addon is for informational purposes only and should not replace professional medical advice. Always consult with your pediatrician regarding your child's development.