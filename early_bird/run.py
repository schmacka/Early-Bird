"""
Early Bird - Main application runner
Flask web server for the Early Bird Home Assistant addon
"""
import json
import os
from flask import Flask, render_template, jsonify, request
from sensor import EarlyBirdSensor
from datetime import datetime

app = Flask(__name__)

# Load configuration from Home Assistant
def load_config():
    """Load configuration from options.json"""
    config_file = '/data/options.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return {
        "child_name": "Baby",
        "birth_date": "2024-01-01",
        "due_date": "2024-03-01",
        "language": "de",
        "notifications_enabled": True
    }

config = load_config()

# Initialize sensor
sensor = None
if config.get('birth_date') and config.get('due_date'):
    sensor = EarlyBirdSensor(
        child_name=config.get('child_name', 'Baby'),
        birth_date=config['birth_date'],
        due_date=config['due_date'],
        data_file='/data/child_data.json'
    )

@app.route('/')
def index():
    """Main dashboard page"""
    if not sensor:
        return render_template('setup.html')
    return render_template('index.html', config=config)

@app.route('/information')
def information_page():
    """Information page for parents"""
    return render_template('information.html', config=config)

@app.route('/api/summary')
def api_summary():
    """Get complete summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.get_summary())

@app.route('/api/encouragement')
def api_encouragement():
    """Get daily encouragement"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.get_daily_encouragement())

@app.route('/api/age')
def api_age():
    """Get corrected and actual age"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.calculate_corrected_age())

@app.route('/api/wonder-weeks')
def api_wonder_weeks():
    """Get Wonder Weeks information"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.get_current_wonder_week())

@app.route('/api/milestones')
def api_milestones():
    """Get upcoming milestones"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    category = request.args.get('category')
    weeks_ahead = int(request.args.get('weeks_ahead', 12))
    return jsonify(sensor.get_upcoming_milestones(category, weeks_ahead))

@app.route('/api/growth', methods=['GET', 'POST'])
def api_growth():
    """Get or add growth records"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    
    if request.method == 'POST':
        data = request.json
        record = sensor.add_growth_record(
            weight_kg=data.get('weight_kg'),
            height_cm=data.get('height_cm'),
            head_circumference_cm=data.get('head_circumference_cm')
        )
        return jsonify(record)
    else:
        return jsonify(sensor.get_growth_history())

@app.route('/api/milestone-achievements', methods=['GET', 'POST'])
def api_milestone_achievements():
    """Get or add milestone achievements"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    
    if request.method == 'POST':
        data = request.json
        achievement = sensor.add_milestone_achievement(
            category=data.get('category'),
            milestone_description=data.get('milestone')
        )
        return jsonify(achievement)
    else:
        return jsonify(sensor.get_milestone_history())

@app.route('/api/u-examinations')
def api_u_examinations():
    """Get U-examinations status"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.get_u_examinations_status())

@app.route('/api/u-examinations/complete', methods=['POST'])
def api_complete_u_examination():
    """Mark U-examination as completed"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    data = request.json
    record = sensor.mark_u_examination_completed(
        exam_name=data.get('exam_name'),
        date=data.get('date'),
        notes=data.get('notes', '')
    )
    return jsonify(record)

# Sleep Pattern Tracking Endpoints

@app.route('/api/sleep', methods=['POST'])
def api_add_sleep():
    """Add sleep record"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    data = request.json
    record = sensor.add_sleep_record(
        sleep_type=data.get('sleep_type'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time'),
        quality=data.get('quality', 'normal'),
        notes=data.get('notes', '')
    )
    return jsonify(record)

@app.route('/api/sleep/summary')
def api_sleep_summary():
    """Get sleep summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    date = request.args.get('date')
    days_back = int(request.args.get('days_back', 7))

    return jsonify(sensor.get_sleep_summary(date, days_back))

@app.route('/api/sleep/records')
def api_sleep_records():
    """Get sleep records"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    limit = int(request.args.get('limit', 50))
    return jsonify({"records": sensor.get_sleep_records(limit)})

# Progress Reminder Endpoints

@app.route('/api/progress-reminder')
def api_progress_reminder():
    """Get progress reminder"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    weeks_back = int(request.args.get('weeks_back', 4))
    return jsonify(sensor.get_progress_reminder(weeks_back))

# Growth Chart Endpoints

@app.route('/api/growth/chart/<measurement_type>')
def api_growth_chart(measurement_type):
    """Get growth chart data"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_growth_chart_data(measurement_type))

@app.route('/api/growth/statistics')
def api_growth_statistics():
    """Get growth statistics"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_growth_statistics())

# Pride Archive Endpoints

@app.route('/api/pride-archive')
def api_pride_archive():
    """Get complete pride archive"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    filter_category = request.args.get('category')
    sort_order = request.args.get('sort', 'desc')

    return jsonify(sensor.get_pride_archive(filter_category, sort_order))

@app.route('/api/pride-archive/monthly/<year_month>')
def api_monthly_summary(year_month):
    """Get monthly summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400

    return jsonify(sensor.get_monthly_summary(year_month))

# Calming Techniques & Bonding Tips Pages

@app.route('/calming-techniques')
def calming_techniques_page():
    """Calming techniques information page"""
    return render_template('calming_techniques.html', config=config)

@app.route('/bonding-tips')
def bonding_tips_page():
    """Bonding tips information page"""
    return render_template('bonding_tips.html', config=config)

@app.route('/archive')
def archive_page():
    """Pride archive timeline page"""
    if not sensor:
        return render_template('setup.html')
    return render_template('archive.html', config=config)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099, debug=False)
