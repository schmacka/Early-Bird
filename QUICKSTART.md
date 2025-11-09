# Early Bird Quick Start Guide

Get started with Early Bird in just 5 minutes!

## Prerequisites

- Home Assistant installed and running
- Supervisor add-ons enabled
- Your child's birth date and due date

## Installation (5 steps)

### Step 1: Install the Addon

1. Open Home Assistant
2. Go to **Supervisor** → **Add-on Store**
3. Click the menu (⋮) → **Repositories**
4. Add this repository URL
5. Find **Early Bird** and click **Install**

### Step 2: Configure

1. Click on **Early Bird** addon
2. Go to **Configuration** tab
3. Fill in the required fields:

```json
{
  "child_name": "Your Baby's Name",
  "birth_date": "2024-01-15",
  "due_date": "2024-03-01",
  "language": "de",
  "notifications_enabled": true
}
```

**Important**: 
- Use format YYYY-MM-DD for dates
- `birth_date`: actual birth date
- `due_date`: original due date from your doctor

### Step 3: Start the Addon

1. Click **Save**
2. Go to **Info** tab
3. Click **Start**
4. Wait for the addon to start (should take less than 30 seconds)

### Step 4: Access the Dashboard

**Option A: Via Ingress (Recommended)**
1. Click **Open Web UI** button
2. The dashboard opens in Home Assistant

**Option B: Direct Access**
1. Go to: `http://homeassistant.local:8099`
2. Or use your HA IP: `http://YOUR_IP:8099`

### Step 5: Start Tracking

You should now see your dashboard with:
- **Age Display**: Corrected and actual age
- **Wonder Weeks**: Current or next developmental leap
- **Milestones**: Upcoming developmental milestones

## First Actions

### Record First Growth Measurement

1. Scroll to "Wachstum erfassen" (Growth Tracking)
2. Enter current weight (kg) and height (cm)
3. Optionally add head circumference (cm)
4. Click **Wachstum speichern** (Save Growth)

### Record a Milestone

1. Scroll to "Meilenstein erfassen" (Milestone Tracking)
2. Select category (Motor/Cognitive/Language)
3. Describe the milestone
4. Click **Meilenstein speichern** (Save Milestone)

## Understanding the Dashboard

### Age Section 📅
- **Korrigiertes Alter**: Corrected age (from due date)
- **Tatsächliches Alter**: Actual age (from birth)
- **Frühgeburt**: How premature your baby was

**Why it matters**: Use corrected age for developmental expectations!

### Wonder Weeks Section 🌟
Shows your baby's current developmental leap or when the next one is coming.

**During a leap**: Your baby might be fussier and need more comfort.

### Milestones Section 🎯
Lists upcoming developmental milestones in the next 12 weeks.

**Example**: "Lifts head when on tummy" - expected in 2 weeks

## Tips for Success

### Daily Use
- Check the dashboard weekly to see progress
- Record growth measurements monthly
- Note milestones when they happen

### Understanding Corrected Age
If your baby was born 8 weeks early:
- At 12 weeks actual age, corrected age is 4 weeks
- Expect 4-week milestones, not 12-week milestones
- This is normal and expected for premature babies!

### Wonder Weeks
During a leap (lasting 1-4 weeks):
- Baby may be fussier than usual
- Sleep might be disrupted
- More clingy behavior is normal
- It's a sign of brain development!

## Troubleshooting

### Can't access dashboard?
- Verify addon is running (Info tab, should say "started")
- Try refreshing your browser
- Check Home Assistant logs

### Wrong dates?
- Stop the addon
- Fix dates in Configuration
- Save and restart

### Data not saving?
- Check browser console for errors
- Verify addon has write permissions
- Check addon logs

## Next Steps

### Add to Home Assistant Dashboard

Create a simple button to access Early Bird:

1. Edit your Lovelace dashboard
2. Add this card:

```yaml
type: button
name: Early Bird
icon: mdi:baby-face
tap_action:
  action: url
  url_path: /api/hassio_ingress/early_bird
```

### Create Sensors (Advanced)

Add REST sensors to display data in Home Assistant:

```yaml
sensor:
  - platform: rest
    name: baby_corrected_age_weeks
    resource: http://localhost:8099/api/age
    value_template: "{{ value_json.corrected_age.total_weeks }}"
    unit_of_measurement: "weeks"
```

See `dashboard_card_example.yaml` for more examples!

## Common Questions

**Q: How accurate are the calculations?**  
A: Age calculations are precise. Milestones are guidelines, not strict deadlines.

**Q: Can I track multiple children?**  
A: Currently supports one child. Multiple children support is planned.

**Q: Is my data private?**  
A: Yes! All data stays in your Home Assistant, never sent anywhere.

**Q: What if I enter wrong data?**  
A: Currently, you'd need to edit the JSON file directly or delete and re-enter.

**Q: Wonder Weeks seems off?**  
A: Remember it's based on corrected age, not actual age!

## Getting Help

- Review full documentation: `DOCS.md`
- Check examples: `dashboard_card_example.yaml`
- Report issues on GitHub
- Ask in Home Assistant community forums

## Enjoy Tracking Your Baby's Development! 🐣

Remember: Every baby develops at their own pace. The timeline is a guide, not a deadline. Consult your pediatrician with any concerns.
