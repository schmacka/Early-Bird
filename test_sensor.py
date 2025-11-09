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

def test_sleep_tracking(sensor):
    """Test sleep pattern tracking - Phase 2 feature"""
    print("Testing sleep pattern tracking...")

    # Add test sleep records
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=10)

    # Add a night sleep
    night_record = sensor.add_sleep_record(
        sleep_type="night",
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        quality="good",
        notes="Slept through the night!"
    )

    print(f"  Added night sleep record: {night_record['duration_hours']} hours")
    assert night_record['duration_hours'] == 10.0, "Duration calculation incorrect"
    assert night_record['sleep_type'] == "night", "Sleep type incorrect"
    assert night_record['quality'] == "good", "Quality incorrect"

    # Add a nap
    nap_start = start_time + timedelta(hours=12)
    nap_end = nap_start + timedelta(hours=2)

    nap_record = sensor.add_sleep_record(
        sleep_type="nap",
        start_time=nap_start.isoformat(),
        end_time=nap_end.isoformat(),
        quality="normal"
    )

    print(f"  Added nap record: {nap_record['duration_hours']} hours")
    assert nap_record['duration_hours'] == 2.0, "Nap duration incorrect"

    # Get sleep summary
    summary = sensor.get_sleep_summary(days_back=7)

    if "no_data" not in summary:
        print(f"  Total sleep hours (7 days): {summary['total_sleep_hours']}")
        print(f"  Average sleep per day: {summary['average_sleep_per_day']} hours")
        print(f"  Quality distribution: {summary['quality_distribution']}")

        # Check expectations are provided
        assert "age_appropriate_expectations" in summary, "No sleep expectations"
        expectations = summary["age_appropriate_expectations"]
        print(f"  Age-appropriate total: {expectations['total_hours']} hours")

    # Get sleep records
    records = sensor.get_sleep_records(limit=10)
    print(f"  Total sleep records: {len(records)}")
    assert len(records) >= 2, "Not all records retrieved"

    print("  ✓ Sleep tracking works!\n")

def test_progress_reminders(sensor):
    """Test progress reminder generation - Phase 2 feature"""
    print("Testing progress reminders...")

    # Add some growth records with different dates
    from datetime import datetime

    # Simulate older record
    old_weight = 3.5
    current_weight = 4.5

    # Get progress reminder
    reminder = sensor.get_progress_reminder(weeks_back=4)

    print(f"  Looking back: {reminder['weeks_back']} weeks")
    print(f"  Current corrected age: {reminder['current_corrected_age_weeks']} weeks")
    print(f"  Past corrected age: {reminder['past_corrected_age_weeks']} weeks")
    print(f"  Milestones achieved: {reminder['milestones_achieved_count']}")

    # Check encouragement message
    assert "encouragement" in reminder, "No encouragement message"
    print(f"  Encouragement: {reminder['encouragement'][:60]}...")

    # Check structure
    assert "target_date" in reminder, "No target date"
    assert "milestones_achieved" in reminder, "No milestones list"

    print("  ✓ Progress reminders work!\n")

def test_growth_statistics(sensor):
    """Test growth chart data and statistics - Phase 2 feature"""
    print("Testing growth statistics and chart data...")

    # Add multiple growth records
    sensor.add_growth_record(weight_kg=3.8, height_cm=50.0, head_circumference_cm=36.0)
    sensor.add_growth_record(weight_kg=4.2, height_cm=51.5, head_circumference_cm=37.0)
    sensor.add_growth_record(weight_kg=4.6, height_cm=53.0, head_circumference_cm=38.0)

    # Get growth statistics
    stats = sensor.get_growth_statistics()

    if "insufficient_data" not in stats:
        print(f"  Total weight gain: {stats['weight_gain_total_kg']} kg")
        print(f"  Weight gain per week: {stats['weight_gain_per_week_g']} g")
        print(f"  Height gain: {stats['height_gain_total_cm']} cm")
        print(f"  Measurement count: {stats['measurement_count']}")
        print(f"  Time span: {stats['time_span_weeks']} weeks")

        assert stats['weight_gain_total_kg'] > 0, "Weight gain should be positive"
        assert stats['height_gain_total_cm'] > 0, "Height gain should be positive"

    # Test chart data for each measurement type
    for measure_type in ["weight", "height", "head_circumference"]:
        chart_data = sensor.get_growth_chart_data(measure_type)

        print(f"  [{measure_type}] Chart data points: {chart_data['count']}")
        print(f"  [{measure_type}] Unit: {chart_data['unit']}")

        assert chart_data['measurement_type'] == measure_type, f"Wrong measurement type for {measure_type}"
        assert len(chart_data['labels']) == chart_data['count'], f"Label count mismatch for {measure_type}"
        assert len(chart_data['values']) == chart_data['count'], f"Value count mismatch for {measure_type}"

    print("  ✓ Growth statistics and chart data work!\n")

def test_pride_archive(sensor):
    """Test pride archive and timeline - Phase 2 feature"""
    print("Testing pride archive...")

    # Get full archive
    archive = sensor.get_pride_archive()

    print(f"  Total events: {archive['total_count']}")
    print(f"  Categories: {archive['categories']}")

    # Verify structure
    assert "events" in archive, "No events in archive"
    assert "total_count" in archive, "No total count"
    assert "categories" in archive, "No categories"
    assert "date_range" in archive, "No date range"

    # Check that events have required fields
    if archive['events']:
        event = archive['events'][0]
        required_fields = ['type', 'category', 'title', 'date', 'icon']
        for field in required_fields:
            assert field in event, f"Missing field: {field} in event"
        print(f"  Sample event: {event['title']} ({event['category']})")

    # Test filtering by category
    motor_archive = sensor.get_pride_archive(filter_category="motor")
    print(f"  Motor events only: {motor_archive['total_count']}")

    # Test sorting
    asc_archive = sensor.get_pride_archive(sort_order="asc")
    desc_archive = sensor.get_pride_archive(sort_order="desc")

    if asc_archive['events'] and desc_archive['events']:
        assert asc_archive['events'][0]['date'] <= asc_archive['events'][-1]['date'], "Ascending sort failed"
        assert desc_archive['events'][0]['date'] >= desc_archive['events'][-1]['date'], "Descending sort failed"
        print("  ✓ Sorting works correctly")

    # Test monthly summary
    year_month = datetime.now().strftime("%Y-%m")
    monthly = sensor.get_monthly_summary(year_month)

    print(f"  Monthly summary for {monthly['year_month']}: {monthly['count']} events")
    assert "events" in monthly, "No events in monthly summary"
    assert "categories" in monthly, "No categories in monthly summary"

    print("  ✓ Pride archive works!\n")

def main():
    print("=" * 60)
    print("Early Bird Sensor Test Suite")
    print("=" * 60 + "\n")

    try:
        # Phase 1 Tests
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

        # Phase 2 Tests
        print("=" * 60)
        print("Phase 2 Feature Tests")
        print("=" * 60 + "\n")

        test_sleep_tracking(sensor)
        test_progress_reminders(sensor)
        test_growth_statistics(sensor)
        test_pride_archive(sensor)

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
