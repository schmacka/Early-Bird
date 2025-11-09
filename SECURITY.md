# Security Policy

## Data Privacy

Early Bird is designed with privacy as a priority:

- **Local Storage Only**: All data is stored locally in your Home Assistant instance
- **No External Services**: The addon does not connect to any external services or APIs
- **No Cloud Sync**: Your child's data never leaves your network
- **No Telemetry**: No usage tracking or analytics

## Data Collected

The addon stores the following information locally:

- Child's name (optional, for display only)
- Birth date and due date (required for age calculations)
- Growth measurements (weight, height, head circumference)
- Milestone achievements with dates
- Timestamps for all records

## Data Storage

- All data is stored in JSON format at `/data/child_data.json`
- Configuration is stored in Home Assistant's addon configuration
- No database connections
- No external file access

## Security Features

1. **AppArmor Profile**: Restricts addon's system access
2. **Ingress Support**: Secure access through Home Assistant's authentication
3. **No Root Required**: Runs with minimal privileges
4. **Input Validation**: All user inputs are validated before storage
5. **Read-Only Templates**: Frontend templates are read-only

## Network Security

- The addon only listens on localhost by default
- When using ingress, Home Assistant's authentication protects access
- No outbound network connections are made
- Port 8099 can be exposed if needed (protected by Home Assistant)

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do not** open a public issue
2. Email the maintainer privately (see repository)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Best Practices

For users:

1. Keep Home Assistant updated
2. Use strong passwords for Home Assistant
3. Enable 2FA on Home Assistant if possible
4. Regular backups of addon data
5. Limit network access to Home Assistant
6. Review addon logs periodically

## Data Retention

- Data is retained indefinitely unless manually deleted
- To delete data:
  1. Stop the addon
  2. Remove `/data/child_data.json`
  3. Restart the addon

## Compliance

- The addon does not collect personal data for processing
- All data remains on your device
- You maintain complete control of your data
- No GDPR compliance required (no data processor)

## Security Audit

Last security review: 2024-11-09

### Known Issues

None currently identified in production code.

### False Positives

- CodeQL alert in `test_sensor.py` for logging test data: This is synthetic test data, not real personal information.

## Updates

Security updates will be released as soon as possible. Keep your addon updated to the latest version.

## Disclaimer

This addon handles personal health information about your child. While we prioritize security:

1. Use at your own risk
2. Always maintain backups
3. Consult security best practices for Home Assistant
4. This is not a medical device
5. The addon is provided as-is without warranty

## Contact

For security concerns, please contact the repository maintainer.
