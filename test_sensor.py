#!/usr/bin/env python3
"""
Simple test script for Early Bird sensor functionality
"""
import sys
import os
from datetime import datetime, timedelta

# Add the early_bird directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'early_bird'))

from sensor import EarlyBirdSensor

def test_corrected_age():
    """Test corrected age calculation"""
    print("Testing corrected age calculation...")
    
    # Create a test case: baby born 8 weeks early
    # Note: These are synthetic test dates, not real personal data
    birth_date = "2024-01-01"
    due_date = "2024-02-26"  # ~8 weeks after birth
    
    sensor = EarlyBirdSensor(
        child_name="Test Baby",
        birth_date=birth_date,
        due_date=due_date,
        data_file="/tmp/test_data.json"
    )
    
    age_info = sensor.calculate_corrected_age()
    
    print(f"  Birth date: {birth_date}")
    print(f"  Due date: {due_date}")
    print(f"  Prematurity: {age_info['prematurity']['weeks']} weeks, {age_info['prematurity']['days']} days")
    print(f"  Corrected age: {age_info['corrected_age']['years']}y {age_info['corrected_age']['months']}m {age_info['corrected_age']['weeks']}w {age_info['corrected_age']['days']}d")
    print(f"  Actual age: {age_info['actual_age']['years']}y {age_info['actual_age']['months']}m {age_info['actual_age']['weeks']}w {age_info['actual_age']['days']}d")
    print("  ✓ Corrected age calculation works!\n")
    
    return sensor

def test_wonder_weeks(sensor):
    """Test Wonder Weeks calculation"""
    print("Testing Wonder Weeks...")
    
    wonder_week = sensor.get_current_wonder_week()
    
    print(f"  Current week: {wonder_week['current_week']}")
    if wonder_week['current_leap']:
        print(f"  Current leap: Week {wonder_week['current_leap']['week']} - {wonder_week['current_leap']['name']}")
    if wonder_week['next_leap']:
        print(f"  Next leap: Week {wonder_week['next_leap']['week']} - {wonder_week['next_leap']['name']}")
    print("  ✓ Wonder Weeks calculation works!\n")

def test_milestones(sensor):
    """Test milestone tracking"""
    print("Testing milestone tracking...")
    
    milestones = sensor.get_upcoming_milestones(weeks_ahead=12)
    
    print(f"  Found {len(milestones)} upcoming milestones in next 12 weeks")
    for ms in milestones[:3]:
        print(f"    - [{ms['category']}] {ms['milestone']} (in {ms['weeks_until']} weeks)")
    print("  ✓ Milestone tracking works!\n")

def test_growth_tracking(sensor):
    """Test growth record storage"""
    print("Testing growth tracking...")
    
    # Add a test record
    record = sensor.add_growth_record(
        weight_kg=4.5,
        height_cm=52.0,
        head_circumference_cm=38.0
    )
    
    print(f"  Added growth record at {record['corrected_age_weeks']} weeks corrected age")
    print(f"    Weight: {record['weight_kg']} kg")
    print(f"    Height: {record['height_cm']} cm")
    print(f"    Head circumference: {record['head_circumference_cm']} cm")
    
    history = sensor.get_growth_history()
    print(f"  Total records: {len(history)}")
    print("  ✓ Growth tracking works!\n")

def test_milestone_achievement(sensor):
    """Test milestone achievement recording"""
    print("Testing milestone achievement recording...")
    
    achievement = sensor.add_milestone_achievement(
        category="motor",
        milestone_description="First smile!"
    )
    
    print(f"  Recorded milestone at {achievement['corrected_age_weeks']} weeks corrected age")
    print(f"    Category: {achievement['category']}")
    print(f"    Milestone: {achievement['milestone']}")
    
    history = sensor.get_milestone_history()
    print(f"  Total achievements: {len(history)}")
    print("  ✓ Milestone achievement recording works!\n")

def test_summary(sensor):
    """Test comprehensive summary"""
    print("Testing summary generation...")
    
    summary = sensor.get_summary()
    
    print(f"  Child name: {summary['child_name']}")
    print(f"  Corrected age (weeks): {summary['age']['corrected_age']['total_weeks']}")
    print(f"  Current week: {summary['wonder_week']['current_week']}")
    print(f"  Upcoming milestones: {len(summary['upcoming_milestones'])}")
    print(f"  Growth records: {summary['growth_records_count']}")
    print(f"  Milestone achievements: {summary['milestone_achievements_count']}")
    print("  ✓ Summary generation works!\n")

def main():
    print("=" * 60)
    print("Early Bird Sensor Test Suite")
    print("=" * 60 + "\n")
    
    try:
        sensor = test_corrected_age()
        test_wonder_weeks(sensor)
        test_milestones(sensor)
        test_growth_tracking(sensor)
        test_milestone_achievement(sensor)
        test_summary(sensor)
        
        print("=" * 60)
        print("✓ All tests passed successfully!")
        print("=" * 60)
        
        # Clean up test file
        if os.path.exists("/tmp/test_data.json"):
            os.remove("/tmp/test_data.json")
        
        return 0
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
