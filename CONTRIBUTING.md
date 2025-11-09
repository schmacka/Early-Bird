# Contributing to Early Bird

Thank you for your interest in contributing to Early Bird! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant (for testing)
- Docker (for building the addon)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/schmacka/Early-Bird.git
cd Early-Bird
```

2. Install Python dependencies:
```bash
pip install -r early_bird/requirements.txt
```

3. Run the test suite:
```bash
python3 test_sensor.py
```

4. Verify installation:
```bash
./verify_installation.sh
```

## Project Structure

```
Early-Bird/
├── early_bird/              # Main addon directory
│   ├── config.json          # Addon configuration
│   ├── Dockerfile           # Container definition
│   ├── run.py              # Flask web application
│   ├── sensor.py           # Core logic (age calculations, milestones)
│   ├── templates/          # HTML templates
│   ├── translations/       # Language files
│   └── DOCS.md            # User documentation
├── test_sensor.py          # Test suite
└── README.md              # Project overview
```

## Making Changes

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

### Testing

Always test your changes:

1. Run the test suite:
```bash
python3 test_sensor.py
```

2. Test with real dates:
```bash
# Edit test_sensor.py with current dates
python3 test_sensor.py
```

3. Test the web interface:
```bash
cd early_bird
python3 run.py
# Access http://localhost:8099
```

### Adding Features

When adding new features:

1. Update `sensor.py` with the core logic
2. Add REST API endpoints in `run.py`
3. Update the UI in `templates/index.html`
4. Add translations to both `de.json` and `en.json`
5. Update documentation in `DOCS.md`
6. Add tests if applicable

## Commit Messages

Use clear, descriptive commit messages:

- `feat: Add new milestone category`
- `fix: Correct age calculation for leap years`
- `docs: Update installation instructions`
- `test: Add tests for wonder weeks calculation`

## Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and verification
5. Commit your changes
6. Push to your fork
7. Open a Pull Request

### PR Checklist

- [ ] Tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Translations updated (if UI changes)
- [ ] CHANGELOG.md updated

## Areas for Contribution

### High Priority

- Additional milestone data (especially for older children)
- Growth chart visualization
- Export functionality (CSV, PDF)
- Enhanced notifications
- Multiple children support
- Backup/restore functionality

### Translations

Help translate Early Bird to more languages:

1. Copy `early_bird/translations/en.json` to `XX.json` (your language code)
2. Translate all strings
3. Update `config.json` to add language option
4. Submit a PR

### Documentation

- Improve user documentation
- Add screenshots
- Create video tutorials
- Translate documentation

### Testing

- Add more test cases
- Test on different Home Assistant versions
- Test on different architectures
- Report bugs

## Medical Accuracy

Early Bird provides developmental tracking information. When contributing medical or developmental information:

1. Cite reliable sources (WHO, AAP, medical journals)
2. Be conservative with milestone timings
3. Include disclaimers where appropriate
4. Consider cultural variations

**Important**: This addon is informational only and should not replace medical advice.

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Review existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn
- Remember this is a project to help parents of premature babies

Thank you for contributing to Early Bird! 🐣
