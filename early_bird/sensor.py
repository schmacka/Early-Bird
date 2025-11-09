"""
Early Bird Sensor - Tracks development of premature children
Includes corrected age calculation, milestone tracking, and Wonder Weeks integration
"""
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import os


class EarlyBirdSensor:
    """Main sensor class for Early Bird addon"""
    
    # Wonder Weeks developmental leaps (weeks from due date)
    WONDER_WEEKS = [
        {"week": 5, "name": "Changing Sensations", "duration": "1-2 weeks"},
        {"week": 8, "name": "Patterns", "duration": "1-2 weeks"},
        {"week": 12, "name": "Smooth Transitions", "duration": "1-2 weeks"},
        {"week": 19, "name": "Events", "duration": "2-3 weeks"},
        {"week": 26, "name": "Relationships", "duration": "2-3 weeks"},
        {"week": 37, "name": "Categories", "duration": "2-3 weeks"},
        {"week": 46, "name": "Sequences", "duration": "2-3 weeks"},
        {"week": 55, "name": "Programs", "duration": "2-3 weeks"},
        {"week": 64, "name": "Principles", "duration": "2-3 weeks"},
        {"week": 75, "name": "Systems", "duration": "2-4 weeks"}
    ]
    
    # Developmental milestones based on corrected age
    MILESTONES = {
        "motor": [
            {"age_weeks": 8, "milestone": "Lifts head when on tummy"},
            {"age_weeks": 12, "milestone": "Holds head steady"},
            {"age_weeks": 16, "milestone": "Rolls from tummy to back"},
            {"age_weeks": 24, "milestone": "Sits without support"},
            {"age_weeks": 32, "milestone": "Crawls"},
            {"age_weeks": 40, "milestone": "Pulls to stand"},
            {"age_weeks": 52, "milestone": "Walks with support"}
        ],
        "cognitive": [
            {"age_weeks": 6, "milestone": "Recognizes parent's face"},
            {"age_weeks": 12, "milestone": "Smiles responsively"},
            {"age_weeks": 16, "milestone": "Reaches for objects"},
            {"age_weeks": 24, "milestone": "Explores objects with hands"},
            {"age_weeks": 32, "milestone": "Responds to own name"},
            {"age_weeks": 40, "milestone": "Plays peek-a-boo"},
            {"age_weeks": 52, "milestone": "Shows object permanence"}
        ],
        "language": [
            {"age_weeks": 8, "milestone": "Coos and makes sounds"},
            {"age_weeks": 16, "milestone": "Babbles"},
            {"age_weeks": 24, "milestone": "Says mama/dada (non-specific)"},
            {"age_weeks": 40, "milestone": "Says mama/dada (specifically)"},
            {"age_weeks": 52, "milestone": "Says first word"},
            {"age_weeks": 78, "milestone": "Says 2-3 word phrases"}
        ]
    }
    
    def __init__(self, child_name, birth_date, due_date, data_file="data/child_data.json"):
        """
        Initialize the Early Bird sensor
        
        Args:
            child_name: Name of the child
            birth_date: Actual birth date (YYYY-MM-DD)
            due_date: Expected due date (YYYY-MM-DD)
            data_file: Path to data storage file
        """
        self.child_name = child_name
        self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self):
        """Load stored data from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            "growth_records": [],
            "milestone_achievements": []
        }
    
    def _save_data(self):
        """Save data to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def calculate_corrected_age(self):
        """
        Calculate corrected age based on due date
        
        Returns:
            dict: Corrected age in years, months, weeks, and days
        """
        today = datetime.now()
        age_from_due = relativedelta(today, self.due_date)
        
        # Calculate total weeks from due date
        total_days = (today - self.due_date).days
        total_weeks = total_days // 7
        remaining_days = total_days % 7
        
        # Calculate actual age from birth
        actual_age = relativedelta(today, self.birth_date)
        actual_age_days = (today - self.birth_date).days
        
        # Calculate prematurity (weeks born early)
        prematurity_days = (self.due_date - self.birth_date).days
        prematurity_weeks = prematurity_days // 7
        
        return {
            "corrected_age": {
                "years": age_from_due.years,
                "months": age_from_due.months,
                "weeks": age_from_due.weeks,
                "days": age_from_due.days,
                "total_weeks": total_weeks,
                "total_days": total_days
            },
            "actual_age": {
                "years": actual_age.years,
                "months": actual_age.months,
                "weeks": actual_age.weeks,
                "days": actual_age.days,
                "total_days": actual_age_days
            },
            "prematurity": {
                "weeks": prematurity_weeks,
                "days": prematurity_days % 7,
                "total_days": prematurity_days
            }
        }
    
    def get_current_wonder_week(self):
        """
        Get current or next Wonder Week based on corrected age
        
        Returns:
            dict: Current/next Wonder Week information
        """
        age_info = self.calculate_corrected_age()
        current_week = age_info["corrected_age"]["total_weeks"]
        
        current_leap = None
        next_leap = None
        
        for leap in self.WONDER_WEEKS:
            if leap["week"] <= current_week <= leap["week"] + 3:
                current_leap = leap
                break
        
        for leap in self.WONDER_WEEKS:
            if leap["week"] > current_week:
                next_leap = leap
                break
        
        return {
            "current_leap": current_leap,
            "next_leap": next_leap,
            "current_week": current_week
        }
    
    def get_upcoming_milestones(self, category=None, weeks_ahead=12):
        """
        Get upcoming milestones based on corrected age
        
        Args:
            category: Optional category filter (motor, cognitive, language)
            weeks_ahead: Number of weeks to look ahead
            
        Returns:
            list: Upcoming milestones
        """
        age_info = self.calculate_corrected_age()
        current_week = age_info["corrected_age"]["total_weeks"]
        
        upcoming = []
        categories = [category] if category else ["motor", "cognitive", "language"]
        
        for cat in categories:
            for milestone in self.MILESTONES[cat]:
                if current_week <= milestone["age_weeks"] <= current_week + weeks_ahead:
                    upcoming.append({
                        "category": cat,
                        "age_weeks": milestone["age_weeks"],
                        "milestone": milestone["milestone"],
                        "weeks_until": milestone["age_weeks"] - current_week
                    })
        
        return sorted(upcoming, key=lambda x: x["age_weeks"])
    
    def add_growth_record(self, weight_kg, height_cm, head_circumference_cm=None):
        """
        Add a growth measurement record
        
        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters
            head_circumference_cm: Optional head circumference in cm
        """
        age_info = self.calculate_corrected_age()
        record = {
            "date": datetime.now().isoformat(),
            "corrected_age_weeks": age_info["corrected_age"]["total_weeks"],
            "actual_age_weeks": age_info["actual_age"]["total_days"] // 7,
            "weight_kg": weight_kg,
            "height_cm": height_cm,
            "head_circumference_cm": head_circumference_cm
        }
        self.data["growth_records"].append(record)
        self._save_data()
        return record
    
    def add_milestone_achievement(self, category, milestone_description):
        """
        Record a milestone achievement
        
        Args:
            category: Category (motor, cognitive, language)
            milestone_description: Description of the milestone
        """
        age_info = self.calculate_corrected_age()
        achievement = {
            "date": datetime.now().isoformat(),
            "corrected_age_weeks": age_info["corrected_age"]["total_weeks"],
            "category": category,
            "milestone": milestone_description
        }
        self.data["milestone_achievements"].append(achievement)
        self._save_data()
        return achievement
    
    def get_growth_history(self):
        """Get all growth records"""
        return self.data.get("growth_records", [])
    
    def get_milestone_history(self):
        """Get all milestone achievements"""
        return self.data.get("milestone_achievements", [])
    
    def get_summary(self):
        """
        Get comprehensive summary of child's development
        
        Returns:
            dict: Complete summary
        """
        age_info = self.calculate_corrected_age()
        wonder_week = self.get_current_wonder_week()
        milestones = self.get_upcoming_milestones()
        
        return {
            "child_name": self.child_name,
            "age": age_info,
            "wonder_week": wonder_week,
            "upcoming_milestones": milestones,
            "growth_records_count": len(self.data.get("growth_records", [])),
            "milestone_achievements_count": len(self.data.get("milestone_achievements", []))
        }
