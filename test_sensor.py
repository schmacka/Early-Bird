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

def test_life_moments(sensor):
    """Test life_moments milestone category"""
    print("Testing life_moments milestone category...")

    # Test that life_moments are included in upcoming milestones
    all_milestones = sensor.get_upcoming_milestones(weeks_ahead=100)
    life_moment_milestones = [m for m in all_milestones if m['category'] == 'life_moments']

    print(f"  Found {len(life_moment_milestones)} life_moments in upcoming milestones")
    if life_moment_milestones:
        first_moment = life_moment_milestones[0]
        print(f"    Next life moment: {first_moment['milestone']} (in {first_moment['weeks_until']} weeks)")

    # Test recording a life_moments achievement
    achievement = sensor.add_milestone_achievement(
        category="life_moments",
        milestone_description="First conscious smile"
    )

    print(f"  Recorded life moment at {achievement['corrected_age_weeks']} weeks")
    print(f"    Milestone: {achievement['milestone']}")

    # Verify it's in the history
    history = sensor.get_milestone_history()
    life_moments_in_history = [m for m in history if m['category'] == 'life_moments']
    print(f"  Total life moments recorded: {len(life_moments_in_history)}")
    print("  ✓ Life moments category works!\n")

def test_congratulation_messages(sensor):
    """Test automatic congratulation message generation"""
    print("Testing congratulation message generation...")

    # Test congratulation for each category
    categories = ["motor", "cognitive", "language", "life_moments"]

    for category in categories:
        achievement = sensor.add_milestone_achievement(
            category=category,
            milestone_description=f"Test {category} milestone"
        )

        # Check that congratulation message was generated
        assert "congratulation" in achievement, f"No congratulation for {category}"
        assert sensor.child_name in achievement["congratulation"], f"Child name not in {category} congratulation"

        print(f"  [{category}] {achievement['congratulation']}")

    print("  ✓ Congratulation messages generated correctly!\n")

def test_encouragement(sensor):
    """Test daily encouragement generation"""
    print("Testing daily encouragement system...")

    # Test basic encouragement generation
    encouragement = sensor.get_daily_encouragement()

    print(f"  Message: {encouragement['message']}")
    print(f"  Context: {encouragement['context']}")

    # Verify message structure
    assert "message" in encouragement, "No message in encouragement"
    assert "context" in encouragement, "No context in encouragement"
    assert "date" in encouragement, "No date in encouragement"
    assert sensor.child_name in encouragement["message"], "Child name not in encouragement"

    # Test that context is valid
    valid_contexts = ["wonder_week_active", "wonder_week_calm", "milestone_upcoming",
                      "milestone_achieved", "general", "premature_specific"]
    assert encouragement["context"] in valid_contexts, f"Invalid context: {encouragement['context']}"

    print("  ✓ Daily encouragement works!\n")

def test_u_examinations(sensor):
    """Test U-examination tracking"""
    print("Testing U-examination system...")

    # Get U-examination status
    status = sensor.get_u_examinations_status()

    print(f"  Total U-examinations: {status['total_count']}")
    print(f"  Completed: {status['completed_count']}")
    print(f"  Current (due now): {len(status['current'])}")
    print(f"  Upcoming: {len(status['upcoming'])}")

    # Verify structure
    assert "past" in status, "No past exams in status"
    assert "current" in status, "No current exams in status"
    assert "upcoming" in status, "No upcoming exams in status"
    assert "completed_count" in status, "No completed count"
    assert "total_count" in status, "No total count"

    # Test marking an examination as completed
    record = sensor.mark_u_examination_completed(
        exam_name="U3",
        notes="Test examination completed successfully"
    )

    print(f"  Marked U3 as completed at {record['corrected_age_weeks']} weeks")
    assert "exam_name" in record, "No exam name in record"
    assert record["exam_name"] == "U3", "Wrong exam name"
    assert "notes" in record, "No notes in record"

    # Verify it appears in completed list
    status_updated = sensor.get_u_examinations_status()
    assert status_updated["completed_count"] == 1, "Completed count not updated"

    print("  ✓ U-examination tracking works!\n")

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

    # Verify daily encouragement is included
    assert "daily_encouragement" in summary, "Daily encouragement not in summary"
    print(f"  Daily encouragement: {summary['daily_encouragement']['message'][:50]}...")

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
        test_life_moments(sensor)
        test_congratulation_messages(sensor)
        test_encouragement(sensor)
        test_u_examinations(sensor)
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
