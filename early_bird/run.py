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

@app.route('/api/summary')
def api_summary():
    """Get complete summary"""
    if not sensor:
        return jsonify({"error": "Sensor not configured"}), 400
    return jsonify(sensor.get_summary())

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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099, debug=False)
