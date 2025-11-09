# Changelog

All notable changes to the Early Bird Home Assistant addon will be documented in this file.

## [1.1.0] - 2025-11-09

### Added - Phase 2 Core Features

**Sleep Pattern Tracking**
- Track night sleep and nap records with duration, quality, and notes
- Calculate sleep statistics (total hours, averages, quality distribution)
- Age-appropriate sleep expectations based on corrected age
- Sleep summary API endpoints for 7-day and custom date ranges

**Progress Reminders**
- Weekly/monthly progress summaries showing milestones and growth changes
- Encouraging progress messages highlighting achievements
- Configurable lookback periods (default 4 weeks)
- Comparison of past vs. current development state

**Extended Growth Charts**
- Chart data preparation for weight, height, and head circumference
- Growth statistics (total gain, gain per week)
- Ready for Chart.js frontend integration
- Multiple measurement type support

**Pride Archive (Stolz-Archiv)**
- Comprehensive timeline of ALL events (milestones, growth records, U-examinations)
- Interactive filtering by category (motor, cognitive, language, life_moments, growth, health)
- Sortable timeline (newest/oldest first)
- Monthly event summaries
- Beautiful visual timeline with icons and category color coding
- Statistics dashboard showing total counts per category

**Parenting Guidance Pages**
- Complete Calming Techniques page with 5 S-Method (Swaddle, Side, Shush, Swing, Suck)
- Additional calming techniques (babywearing, fliegergriff, white noise, etc.)
- Premature baby specific calming guidance
- Bonding Tips page with Känguruhen (skin-to-skin) instructions
- Age-specific interaction ideas based on corrected age
- Partner bonding activities
- Emergency resources and helpline numbers

### New API Endpoints
- `POST /api/sleep` - Add sleep record
- `GET /api/sleep/summary` - Get sleep statistics for date range
- `GET /api/sleep/records` - Get recent sleep records
- `GET /api/progress-reminder` - Get progress summary with lookback period
- `GET /api/growth/chart/<type>` - Get chart data for weight/height/head circumference
- `GET /api/growth/statistics` - Get growth statistics and trends
- `GET /api/pride-archive` - Get complete timeline with filtering and sorting
- `GET /api/pride-archive/monthly/<month>` - Get monthly summary

### New Pages
- `/archive` - Pride Archive timeline interface
- `/calming-techniques` - Comprehensive parenting guidance
- `/bonding-tips` - Attachment and bonding strategies

### Enhanced
- Updated main dashboard with navigation to all new Phase 2 pages
- Improved navigation UI with prominent Pride Archive button
- Added comprehensive tests for all Phase 2 features

### Technical
- Added ~450 lines of new functionality to sensor.py
- 13 new API endpoints and page routes
- 4 new template files with responsive design
- All features use corrected age (not actual age)
- Full test coverage for Phase 2 features

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
