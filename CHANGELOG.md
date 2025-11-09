# Changelog

All notable changes to the Early Bird Home Assistant addon will be documented in this file.

## [1.0.0] - 2024-11-09

### Added
- Initial release of Early Bird addon
- Corrected age calculator based on due date vs birth date
- Wonder Weeks integration with 10 developmental leaps
- Milestone tracking for motor, cognitive, and language development
- Growth monitoring with weight, height, and head circumference tracking
- Local JSON-based data storage
- Web dashboard with real-time updates
- REST API for integration
- German language support (primary)
- English language support
- Home Assistant notifications (framework ready)
- Responsive web interface
- Setup wizard for initial configuration

### Features
- Automatic corrected age calculation
- Display both corrected and actual age
- Track prematurity offset
- Wonder Weeks leap detection and countdown
- Upcoming milestone predictions (12 weeks ahead)
- Growth record history
- Milestone achievement history
- Easy-to-use forms for data entry
- Beautiful gradient UI design

### Technical
- Python 3.11 backend
- Flask web framework
- Alpine Linux container
- Multi-architecture support (amd64, armhf, armv7, aarch64, i386)
- Docker-based deployment
- RESTful API endpoints
- JSON configuration schema
