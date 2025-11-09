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
        ],
        "life_moments": [
            {"age_weeks": 4, "milestone": "First conscious smile"},
            {"age_weeks": 6, "milestone": "First night with 4+ hours sleep"},
            {"age_weeks": 12, "milestone": "First laugh"},
            {"age_weeks": 16, "milestone": "Recognizes siblings/pets"},
            {"age_weeks": 20, "milestone": "First solid food meal"},
            {"age_weeks": 24, "milestone": "First tear while laughing"},
            {"age_weeks": 32, "milestone": "Waves goodbye"},
            {"age_weeks": 36, "milestone": "Plays peek-a-boo"},
            {"age_weeks": 40, "milestone": "Claps hands"},
            {"age_weeks": 44, "milestone": "Points with finger"},
            {"age_weeks": 48, "milestone": "Gives kisses"},
            {"age_weeks": 52, "milestone": "Says 'Mama' or 'Papa' intentionally"},
            {"age_weeks": 60, "milestone": "Dances to music"},
            {"age_weeks": 68, "milestone": "Hugs spontaneously"},
            {"age_weeks": 78, "milestone": "Says 'I love you'"}
        ]
    }

    # Congratulation messages for milestone achievements
    CONGRATULATION_TEMPLATES = {
        "motor": [
            "{name} hat einen wichtigen motorischen Meilenstein erreicht! 🎉",
            "Großartig! {name} macht große Fortschritte in der Bewegung!",
            "Welch ein Erfolg! {name} entwickelt sich wunderbar!"
        ],
        "cognitive": [
            "{name} wird immer aufmerksamer! Toll! 🌟",
            "Fantastisch! {name} zeigt tolle kognitive Entwicklung!",
            "Das ist ein wichtiger Entwicklungsschritt für {name}!"
        ],
        "language": [
            "{name} kommuniziert immer mehr! Wunderbar! 💬",
            "Wie schön! {name} macht sprachliche Fortschritte!",
            "Ein wichtiger Meilenstein in {name}s Sprachentwicklung!"
        ],
        "life_moments": [
            "Was für ein besonderer Moment mit {name}! ❤️",
            "{name} schenkt euch unvergessliche Momente!",
            "Diese Erinnerung an {name} ist etwas Besonderes!"
        ]
    }

    # Context-aware encouragement messages
    ENCOURAGEMENTS = {
        "wonder_week_active": [
            "Entwicklungssprünge sind anstrengend, aber {name} macht große Fortschritte!",
            "Diese schwierige Phase geht vorüber. {name} lernt gerade so viel!",
            "Ihr macht das großartig! Wonder Weeks sind intensiv, aber wichtig.",
            "Jeder Entwicklungssprung bringt {name} weiter. Bleibt geduldig!",
            "{name} verarbeitet gerade viele neue Eindrücke. Gebt euch Zeit."
        ],
        "wonder_week_calm": [
            "Genießt diese ruhigere Phase mit {name}!",
            "{name} festigt gerade die neu gelernten Fähigkeiten.",
            "Diese sonnige Phase ist perfekt zum Erkunden und Spielen!",
            "Nutzt diese Zeit für schöne gemeinsame Momente."
        ],
        "milestone_upcoming": [
            "Ein spannender Meilenstein steht bevor! Seid gespannt!",
            "Bald ist es soweit - {name} entwickelt sich wunderbar!",
            "Jedes Kind entwickelt sich in seinem eigenen Tempo. {name} ist genau richtig."
        ],
        "milestone_achieved": [
            "Ihr dürft stolz sein! {name} macht tolle Fortschritte!",
            "Jeder Meilenstein ist ein Grund zum Feiern!",
            "Wunderbar! {name} entwickelt sich prächtig!"
        ],
        "general": [
            "Ihr seid großartige Eltern für {name}!",
            "Vertraut eurem Instinkt - ihr kennt {name} am besten.",
            "Jeder Tag mit {name} ist besonders.",
            "Die ersten Monate sind herausfordernd. Ihr macht das toll!",
            "Frühchen brauchen Zeit. {name} entwickelt sich nach eigenem Tempo.",
            "Korrigiertes Alter macht den Unterschied. {name} ist genau richtig!"
        ],
        "premature_specific": [
            "{name} ist ein kleiner Kämpfer und ihr seid ein starkes Team!",
            "Frühchen holen auf - gebt {name} die Zeit, die er/sie braucht.",
            "Jeder Tag seit der Geburt ist ein Geschenk. {name} ist stark!",
            "Als Frühchen-Eltern leistet ihr Außergewöhnliches!"
        ]
    }

    # U-examination schedule (based on corrected age)
    U_EXAMINATIONS = [
        {
            "name": "U1",
            "age_weeks_min": 0,
            "age_weeks_max": 0.14,
            "description": "Direkt nach der Geburt",
            "checks": ["Atmung, Herzschlag, Hautfarbe", "Reflexe und Muskelspannung", "APGAR-Score"]
        },
        {
            "name": "U2",
            "age_weeks_min": 0.43,
            "age_weeks_max": 1.43,
            "description": "3. bis 10. Lebenstag",
            "checks": ["Gelbsucht-Check", "Hüftultraschall", "Neugeborenen-Screening", "Hörtest"]
        },
        {
            "name": "U3",
            "age_weeks_min": 4,
            "age_weeks_max": 5,
            "description": "4. bis 5. Lebenswoche",
            "checks": ["Gewicht, Größe, Kopfumfang", "Hüftentwicklung", "Seh- und Hörvermögen", "Motorische Entwicklung"]
        },
        {
            "name": "U4",
            "age_weeks_min": 12,
            "age_weeks_max": 16,
            "description": "3. bis 4. Lebensmonat",
            "checks": ["Beweglichkeit und Körperbeherrschung", "Seh- und Hörvermögen", "Hand-Augen-Koordination", "Erste Impfungen"]
        },
        {
            "name": "U5",
            "age_weeks_min": 24,
            "age_weeks_max": 28,
            "description": "6. bis 7. Lebensmonat",
            "checks": ["Bewegungsentwicklung (Drehen, Greifen)", "Sprachentwicklung (Lallen)", "Sozialverhalten", "Weitere Impfungen"]
        },
        {
            "name": "U6",
            "age_weeks_min": 40,
            "age_weeks_max": 48,
            "description": "10. bis 12. Lebensmonat",
            "checks": ["Krabbeln, Sitzen, Stehen", "Feinmotorik (Pinzettengriff)", "Erste Worte", "Impfungen vervollständigen"]
        },
        {
            "name": "U7",
            "age_weeks_min": 88,
            "age_weeks_max": 104,
            "description": "21. bis 24. Lebensmonat",
            "checks": ["Laufen und Geschicklichkeit", "Sprachentwicklung", "Soziales Verhalten", "Entwicklung der Selbständigkeit"]
        },
        {
            "name": "U7a",
            "age_weeks_min": 139,
            "age_weeks_max": 156,
            "description": "34. bis 36. Lebensmonat",
            "checks": ["Sehen, Hören, Sprechen", "Bewegung und Geschicklichkeit", "Soziale und emotionale Entwicklung", "Allergie-Vorsorge"]
        },
        {
            "name": "U8",
            "age_weeks_min": 192,
            "age_weeks_max": 208,
            "description": "46. bis 48. Lebensmonat",
            "checks": ["Körperliche Entwicklung", "Sprachliche Entwicklung", "Verhalten in der Familie", "Vorbereitung auf Kindergarten/Schule"]
        },
        {
            "name": "U9",
            "age_weeks_min": 260,
            "age_weeks_max": 273,
            "description": "60. bis 64. Lebensmonat",
            "checks": ["Schulreife", "Seh- und Hörvermögen", "Sprachentwicklung", "Sozialverhalten und Selbständigkeit"]
        }
    ]

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
        categories = [category] if category else ["motor", "cognitive", "language", "life_moments"]
        
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
    
    def add_milestone_achievement(self, category, milestone_description, notes=""):
        """
        Record a milestone achievement with automatic congratulation

        Args:
            category: Category (motor, cognitive, language, life_moments)
            milestone_description: Description of the milestone
            notes: Optional notes about the achievement

        Returns:
            dict: Achievement record including congratulation message
        """
        import random

        age_info = self.calculate_corrected_age()
        achievement = {
            "date": datetime.now().isoformat(),
            "corrected_age_weeks": age_info["corrected_age"]["total_weeks"],
            "category": category,
            "milestone": milestone_description,
            "notes": notes
        }

        # Generate congratulation message
        templates = self.CONGRATULATION_TEMPLATES.get(category, [])
        if templates:
            achievement["congratulation"] = random.choice(templates).format(
                name=self.child_name
            )

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
            "milestone_achievements_count": len(self.data.get("milestone_achievements", [])),
            "daily_encouragement": self.get_daily_encouragement()
        }

    def get_daily_encouragement(self):
        """
        Get contextual encouragement based on current situation

        Returns:
            dict: Encouragement message with context
        """
        import random

        context = "general"

        # Check Wonder Week status
        current_ww = self.get_current_wonder_week()
        if current_ww and current_ww.get("current_leap"):
            context = "wonder_week_active"
        elif current_ww and current_ww.get("next_leap"):
            weeks_until = current_ww["next_leap"]["week"] - current_ww["current_week"]
            if weeks_until > 2:
                context = "wonder_week_calm"

        # Check recent milestone achievements (last 7 days)
        recent_achievements = [
            a for a in self.data.get("milestone_achievements", [])
            if (datetime.now() - datetime.fromisoformat(a["date"])).days <= 7
        ]
        if recent_achievements:
            context = "milestone_achieved"

        # Check upcoming milestones (next 2 weeks)
        upcoming = self.get_upcoming_milestones(weeks_ahead=2)
        if upcoming and context not in ["milestone_achieved", "wonder_week_active"]:
            context = "milestone_upcoming"

        # Check if very premature (>6 weeks early)
        prematurity_days = (self.due_date - self.birth_date).days
        prematurity_weeks = prematurity_days / 7
        if prematurity_weeks > 6 and random.random() < 0.3:
            context = "premature_specific"

        messages = self.ENCOURAGEMENTS.get(context, self.ENCOURAGEMENTS["general"])
        message = random.choice(messages).format(name=self.child_name)

        return {
            "message": message,
            "context": context,
            "date": datetime.now().isoformat()
        }

    def get_u_examinations_status(self):
        """
        Get status of all U-examinations based on corrected age

        Returns:
            dict: Past, current, upcoming, and completed U-examinations
        """
        corrected_weeks = self._calculate_weeks_from_due()
        completed_exams = self.data.get("u_examinations_completed", [])

        past = []
        current = []
        upcoming = []
        future = []

        for exam in self.U_EXAMINATIONS:
            exam_data = {
                **exam,
                "is_completed": exam["name"] in completed_exams,
                "corrected_age_suitable": False,
                "status": "future"
            }

            if corrected_weeks < exam["age_weeks_min"]:
                exam_data["status"] = "future"
                exam_data["weeks_until"] = exam["age_weeks_min"] - corrected_weeks
                future.append(exam_data)
            elif exam["age_weeks_min"] <= corrected_weeks <= exam["age_weeks_max"]:
                exam_data["status"] = "current"
                exam_data["corrected_age_suitable"] = True
                exam_data["weeks_remaining"] = exam["age_weeks_max"] - corrected_weeks
                current.append(exam_data)
            else:
                exam_data["status"] = "past"
                past.append(exam_data)

        return {
            "past": past,
            "current": current,
            "upcoming": future[:3],
            "completed_count": len(completed_exams),
            "total_count": len(self.U_EXAMINATIONS)
        }

    def mark_u_examination_completed(self, exam_name, date=None, notes=""):
        """
        Mark a U-examination as completed

        Args:
            exam_name: Name of examination (e.g., "U3")
            date: Date of examination (ISO format) or None for today
            notes: Optional notes from the examination

        Returns:
            dict: Updated examination record
        """
        if "u_examinations_completed" not in self.data:
            self.data["u_examinations_completed"] = []

        if "u_examinations_records" not in self.data:
            self.data["u_examinations_records"] = []

        # Don't add duplicates
        if exam_name not in self.data["u_examinations_completed"]:
            self.data["u_examinations_completed"].append(exam_name)

        record = {
            "exam_name": exam_name,
            "date": date or datetime.now().isoformat(),
            "corrected_age_weeks": self._calculate_weeks_from_due(),
            "notes": notes
        }

        self.data["u_examinations_records"].append(record)
        self._save_data()

        return record

    def _calculate_weeks_from_due(self):
        """Helper method to calculate weeks from due date"""
        today = datetime.now()
        total_days = (today - self.due_date).days
        return total_days // 7
