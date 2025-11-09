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

    # Sleep Pattern Tracking Methods

    def add_sleep_record(self, sleep_type, start_time, end_time, quality="normal", notes=""):
        """
        Add sleep record

        Args:
            sleep_type: "night" or "nap"
            start_time: ISO format datetime
            end_time: ISO format datetime
            quality: "poor", "normal", "good"
            notes: Optional notes

        Returns:
            dict: Sleep record with duration calculated
        """
        if "sleep_records" not in self.data:
            self.data["sleep_records"] = []

        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration_hours = (end - start).total_seconds() / 3600

        record = {
            "sleep_type": sleep_type,
            "start_time": start_time,
            "end_time": end_time,
            "duration_hours": round(duration_hours, 2),
            "quality": quality,
            "notes": notes,
            "date": start.date().isoformat(),
            "corrected_age_weeks": self._calculate_weeks_from_due()
        }

        self.data["sleep_records"].append(record)
        self._save_data()

        return record

    def get_sleep_summary(self, date=None, days_back=7):
        """
        Get sleep summary for date range

        Args:
            date: Target date (ISO format) or None for today
            days_back: Number of days to include

        Returns:
            dict: Sleep statistics and patterns
        """
        if not date:
            date = datetime.now().date().isoformat()

        target_date = datetime.fromisoformat(date).date()
        start_date = target_date - timedelta(days=days_back)

        records = self.data.get("sleep_records", [])

        # Filter records in range
        relevant_records = [
            r for r in records
            if start_date <= datetime.fromisoformat(r["date"]).date() <= target_date
        ]

        if not relevant_records:
            return {"no_data": True}

        # Calculate statistics
        total_sleep_hours = sum(r["duration_hours"] for r in relevant_records)
        night_sleep = [r for r in relevant_records if r["sleep_type"] == "night"]
        naps = [r for r in relevant_records if r["sleep_type"] == "nap"]

        avg_night_sleep = sum(r["duration_hours"] for r in night_sleep) / len(night_sleep) if night_sleep else 0
        avg_naps_per_day = len(naps) / days_back
        avg_total_sleep = total_sleep_hours / days_back

        return {
            "date_range": {
                "start": start_date.isoformat(),
                "end": target_date.isoformat()
            },
            "total_sleep_hours": round(total_sleep_hours, 1),
            "average_sleep_per_day": round(avg_total_sleep, 1),
            "average_night_sleep": round(avg_night_sleep, 1),
            "average_naps_per_day": round(avg_naps_per_day, 1),
            "total_nights": len(night_sleep),
            "total_naps": len(naps),
            "quality_distribution": self._calculate_quality_distribution(relevant_records),
            "age_appropriate_expectations": self._get_sleep_expectations()
        }

    def _calculate_quality_distribution(self, records):
        """Calculate distribution of sleep quality"""
        distribution = {"poor": 0, "normal": 0, "good": 0}
        for record in records:
            quality = record.get("quality", "normal")
            distribution[quality] = distribution.get(quality, 0) + 1
        return distribution

    def _get_sleep_expectations(self):
        """Get age-appropriate sleep expectations"""
        corrected_weeks = self._calculate_weeks_from_due()

        if corrected_weeks < 6:
            return {
                "total_hours": "16-20",
                "night_hours": "8-10 (mit Unterbrechungen)",
                "naps": "4-5 pro Tag",
                "note": "Neugeborene schlafen viel, aber in kurzen Intervallen"
            }
        elif corrected_weeks < 16:
            return {
                "total_hours": "14-17",
                "night_hours": "9-10",
                "naps": "3-4 pro Tag",
                "note": "Schlafphasen werden allmählich länger"
            }
        elif corrected_weeks < 26:
            return {
                "total_hours": "14-16",
                "night_hours": "10-11",
                "naps": "2-3 pro Tag",
                "note": "Nachtschlaf wird kontinuierlicher"
            }
        elif corrected_weeks < 52:
            return {
                "total_hours": "12-15",
                "night_hours": "11-12",
                "naps": "2 pro Tag",
                "note": "Etablierung eines regelmäßigen Schlafrhythmus"
            }
        else:
            return {
                "total_hours": "11-14",
                "night_hours": "11-12",
                "naps": "1-2 pro Tag",
                "note": "Übergang zu einem Mittagsschlaf"
            }

    def get_sleep_records(self, limit=50):
        """Get recent sleep records"""
        records = self.data.get("sleep_records", [])
        records_sorted = sorted(records, key=lambda x: x["start_time"], reverse=True)
        return records_sorted[:limit]

    # Progress Reminders Methods

    def get_progress_reminder(self, weeks_back=4):
        """
        Generate progress reminder showing growth over time

        Args:
            weeks_back: How many weeks to look back

        Returns:
            dict: Progress summary with comparisons
        """
        target_date = datetime.now() - timedelta(weeks=weeks_back)

        # Current state
        current_corrected_weeks = self._calculate_weeks_from_due()
        current_ww = self.get_current_wonder_week()

        # Milestones achieved in period
        achievements = [
            a for a in self.data.get("milestone_achievements", [])
            if datetime.fromisoformat(a["date"]) >= target_date
        ]

        # Growth changes
        growth_records = self.data.get("growth_records", [])
        growth_sorted = sorted(growth_records, key=lambda x: x["date"])

        past_record = None
        for record in growth_sorted:
            if datetime.fromisoformat(record["date"]) <= target_date:
                past_record = record

        current_record = growth_sorted[-1] if growth_sorted else None

        growth_change = None
        if past_record and current_record:
            growth_change = {
                "weight_gain_kg": round(current_record.get("weight_kg", 0) - past_record.get("weight_kg", 0), 2),
                "height_gain_cm": round(current_record.get("height_cm", 0) - past_record.get("height_cm", 0), 1),
                "head_gain_cm": round(current_record.get("head_circumference_cm", 0) - past_record.get("head_circumference_cm", 0), 1)
            }

        return {
            "weeks_back": weeks_back,
            "target_date": target_date.isoformat(),
            "current_corrected_age_weeks": current_corrected_weeks,
            "past_corrected_age_weeks": current_corrected_weeks - weeks_back,
            "milestones_achieved_count": len(achievements),
            "milestones_achieved": achievements,
            "growth_change": growth_change,
            "current_wonder_week": current_ww.get("current_leap")["name"] if current_ww.get("current_leap") else None,
            "encouragement": self._get_progress_encouragement(len(achievements), growth_change)
        }

    def _get_progress_encouragement(self, milestone_count, growth_change):
        """Generate encouraging message based on progress"""
        messages = []

        if milestone_count > 0:
            messages.append(f"{self.child_name} hat {milestone_count} neue Meilensteine erreicht!")

        if growth_change and growth_change.get("weight_gain_kg", 0) > 0:
            messages.append(f"{self.child_name} ist {growth_change['weight_gain_kg']} kg gewachsen!")

        if growth_change and growth_change.get("height_gain_cm", 0) > 0:
            messages.append(f"{self.child_name} ist {growth_change['height_gain_cm']} cm größer geworden!")

        if not messages:
            messages.append(f"{self.child_name} entwickelt sich stetig weiter - jeder Tag zählt!")

        return " ".join(messages)

    # Growth Chart Data Methods

    def get_growth_chart_data(self, measurement_type="weight"):
        """
        Get formatted data for growth charts

        Args:
            measurement_type: "weight", "height", or "head_circumference"

        Returns:
            dict: Chart data with labels and values
        """
        records = self.data.get("growth_records", [])

        # Sort by date
        records_sorted = sorted(records, key=lambda x: x["date"])

        labels = []
        values = []
        corrected_ages = []

        field_map = {
            "weight": "weight_kg",
            "height": "height_cm",
            "head_circumference": "head_circumference_cm"
        }

        field = field_map.get(measurement_type, "weight_kg")

        for record in records_sorted:
            if field in record and record[field] is not None:
                labels.append(record["date"])
                values.append(record[field])
                corrected_ages.append(record.get("corrected_age_weeks", 0))

        return {
            "labels": labels,
            "values": values,
            "corrected_ages": corrected_ages,
            "measurement_type": measurement_type,
            "unit": self._get_measurement_unit(measurement_type),
            "count": len(values)
        }

    def _get_measurement_unit(self, measurement_type):
        """Get unit for measurement type"""
        units = {
            "weight": "kg",
            "height": "cm",
            "head_circumference": "cm"
        }
        return units.get(measurement_type, "")

    def get_growth_statistics(self):
        """
        Calculate growth statistics

        Returns:
            dict: Growth trends and statistics
        """
        records = self.data.get("growth_records", [])

        if len(records) < 2:
            return {"insufficient_data": True}

        records_sorted = sorted(records, key=lambda x: x["date"])

        # Calculate weight gain
        first_weight = records_sorted[0].get("weight_kg")
        last_weight = records_sorted[-1].get("weight_kg")
        weight_gain = last_weight - first_weight if first_weight and last_weight else None

        # Calculate height gain
        first_height = records_sorted[0].get("height_cm")
        last_height = records_sorted[-1].get("height_cm")
        height_gain = last_height - first_height if first_height and last_height else None

        # Time span
        first_date = datetime.fromisoformat(records_sorted[0]["date"])
        last_date = datetime.fromisoformat(records_sorted[-1]["date"])
        days_span = (last_date - first_date).days
        weeks_span = days_span / 7

        return {
            "weight_gain_total_kg": round(weight_gain, 2) if weight_gain else None,
            "weight_gain_per_week_g": round((weight_gain / weeks_span) * 1000, 1) if weight_gain and weeks_span > 0 else None,
            "height_gain_total_cm": round(height_gain, 1) if height_gain else None,
            "height_gain_per_week_cm": round(height_gain / weeks_span, 2) if height_gain and weeks_span > 0 else None,
            "measurement_count": len(records),
            "time_span_weeks": round(weeks_span, 1),
            "latest_measurement": records_sorted[-1]
        }

    # Pride Archive Methods

    def get_pride_archive(self, filter_category=None, sort_order="desc"):
        """
        Get comprehensive timeline of all achievements and events

        Args:
            filter_category: Optional filter (motor, cognitive, language, life_moments, growth)
            sort_order: "asc" for chronological, "desc" for reverse chronological

        Returns:
            dict: Timeline events with metadata
        """
        events = []

        # Add milestone achievements
        for achievement in self.data.get("milestone_achievements", []):
            events.append({
                "type": "milestone",
                "category": achievement["category"],
                "title": achievement["milestone"],
                "date": achievement["date"],
                "corrected_age_weeks": achievement.get("corrected_age_weeks", 0),
                "notes": achievement.get("notes", ""),
                "icon": self._get_category_icon(achievement["category"])
            })

        # Add growth records
        for record in self.data.get("growth_records", []):
            events.append({
                "type": "growth",
                "category": "growth",
                "title": f"Wachstumsmessung: {record.get('weight_kg', 'N/A')} kg",
                "date": record["date"],
                "corrected_age_weeks": record.get("corrected_age_weeks", 0),
                "notes": f"Größe: {record.get('height_cm', 'N/A')} cm, Kopfumfang: {record.get('head_circumference_cm', 'N/A')} cm",
                "icon": "📏",
                "data": record
            })

        # Add U-examinations if completed
        for exam in self.data.get("u_examinations_records", []):
            events.append({
                "type": "u_examination",
                "category": "health",
                "title": f"{exam['exam_name']} Untersuchung",
                "date": exam["date"],
                "corrected_age_weeks": exam.get("corrected_age_weeks", 0),
                "notes": exam.get("notes", ""),
                "icon": "🏥"
            })

        # Filter by category if requested
        if filter_category:
            events = [e for e in events if e["category"] == filter_category]

        # Sort by date
        events.sort(key=lambda x: x["date"], reverse=(sort_order == "desc"))

        return {
            "events": events,
            "total_count": len(events),
            "categories": self._get_event_categories(events),
            "date_range": self._get_date_range(events)
        }

    def _get_category_icon(self, category):
        """Get icon for category"""
        icons = {
            "motor": "🏃",
            "cognitive": "🧠",
            "language": "💬",
            "life_moments": "❤️",
            "growth": "📏",
            "health": "🏥"
        }
        return icons.get(category, "⭐")

    def _get_event_categories(self, events):
        """Get unique categories with counts"""
        categories = {}
        for event in events:
            cat = event["category"]
            categories[cat] = categories.get(cat, 0) + 1
        return categories

    def _get_date_range(self, events):
        """Get date range of events"""
        if not events:
            return {"start": None, "end": None}

        dates = [datetime.fromisoformat(e["date"]) for e in events]
        return {
            "start": min(dates).isoformat(),
            "end": max(dates).isoformat()
        }

    def get_monthly_summary(self, year_month=None):
        """
        Get summary of events for a specific month

        Args:
            year_month: "YYYY-MM" format, defaults to current month

        Returns:
            dict: Monthly achievements and statistics
        """
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")

        year, month = map(int, year_month.split("-"))

        archive = self.get_pride_archive()
        month_events = [
            e for e in archive["events"]
            if datetime.fromisoformat(e["date"]).year == year
            and datetime.fromisoformat(e["date"]).month == month
        ]

        return {
            "year_month": year_month,
            "events": month_events,
            "count": len(month_events),
            "categories": self._get_event_categories(month_events)
        }
