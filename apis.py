#!/usr/bin/env python3
"""
Workout Tracker Backend API
Flask-based REST API for the workout tracker application.
Includes Workout Reminder functionality and Weekly Goals Tracker.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import datetime
from typing import Dict, List, Optional
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

class WorkoutTracker:
    def __init__(self, data_file: str = "workouts.json"):
        self.data_file = data_file
        self.reminder_file = "reminders.json"
        self.goals_file = "goals.json"
        self.workouts = self.load_data()
        self.reminders = self.load_reminders()
        self.weekly_goal = self.load_goals()
    
    def load_data(self) -> List[Dict]:
        """Load workout data from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_data(self) -> None:
        """Save workout data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.workouts, f, indent=2, default=str)

    def load_reminders(self) -> List[Dict]:
        """Load reminders from a JSON file."""
        if os.path.exists(self.reminder_file):
            try:
                with open(self.reminder_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_reminders(self) -> None:
        """Save reminders to a JSON file."""
        with open(self.reminder_file, 'w') as f:
            json.dump(self.reminders, f, indent=2, default=str)

    def add_reminder(self, date: str, message: str) -> Dict:
        """Add a new workout reminder."""
        reminder = {
            "id": len(self.reminders) + 1,
            "date": date,
            "message": message
        }
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder

    def get_upcoming_reminders(self) -> List[Dict]:
        """Get reminders with a date in the future."""
        now = datetime.datetime.now()
        upcoming = [
            r for r in self.reminders 
            if datetime.datetime.fromisoformat(r['date']) > now
        ]
        return sorted(upcoming, key=lambda x: x['date'])

    def add_workout(self, workout_type: str, duration: int, exercises: List[Dict], 
                   notes: str = "", date: str = None) -> Dict:
        """Add a new workout session."""
        if date is None:
            date = datetime.datetime.now().isoformat()
        
        workout = {
            "id": len(self.workouts) + 1,
            "date": date,
            "type": workout_type,
            "duration_minutes": duration,
            "exercises": exercises,
            "notes": notes,
            "total_calories": self.calculate_calories(exercises, duration)
        }
        
        self.workouts.append(workout)
        self.save_data()
        return workout
    
    def calculate_calories(self, exercises: List[Dict], duration: int) -> int:
        """Estimate calories burned based on exercises and duration."""
        base_rate = 5  # calories per minute base rate
        intensity_multiplier = 1.0
        
        for exercise in exercises:
            exercise_name = exercise.get('name', '').lower()
            if any(cardio in exercise_name for cardio in ['run', 'cardio', 'cycle', 'swim', 'jog']):
                intensity_multiplier += 0.3
            elif any(strength in exercise_name for strength in ['lift', 'weight', 'strength', 'resistance']):
                intensity_multiplier += 0.2
        
        return int(duration * base_rate * intensity_multiplier)
    
    def get_workouts(self, limit: int = None) -> List[Dict]:
        """Get workouts sorted by date (most recent first)."""
        sorted_workouts = sorted(self.workouts, key=lambda x: x['date'], reverse=True)
        return sorted_workouts[:limit] if limit else sorted_workouts
    
    def get_workout_by_id(self, workout_id: int) -> Optional[Dict]:
        """Get a specific workout by ID."""
        return next((w for w in self.workouts if w['id'] == workout_id), None)
    
    def delete_workout(self, workout_id: int) -> bool:
        """Delete a workout by ID."""
        initial_count = len(self.workouts)
        self.workouts = [w for w in self.workouts if w['id'] != workout_id]
        
        if len(self.workouts) < initial_count:
            self.save_data()
            return True
        return False
    
    def get_stats(self) -> Dict:
        """Get workout statistics."""
        if not self.workouts:
            return {
                "total_workouts": 0,
                "total_duration": 0,
                "total_calories": 0,
                "average_duration": 0,
                "recent_workouts_30d": 0,
                "workout_types": {}
            }
        
        total_workouts = len(self.workouts)
        total_duration = sum(w['duration_minutes'] for w in self.workouts)
        total_calories = sum(w['total_calories'] for w in self.workouts)
        
        thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        recent_workouts = [
            w for w in self.workouts 
            if datetime.datetime.fromisoformat(w['date']) > thirty_days_ago
        ]
        
        workout_types = {}
        for workout in self.workouts:
            workout_type = workout['type']
            workout_types[workout_type] = workout_types.get(workout_type, 0) + 1
        
        return {
            "total_workouts": total_workouts,
            "total_duration": total_duration,
            "total_calories": total_calories,
            "average_duration": total_duration // total_workouts if total_workouts > 0 else 0,
            "recent_workouts_30d": len(recent_workouts),
            "workout_types": workout_types
        }

    # --- Weekly Goals and Progress Feature ---

    def load_goals(self) -> Dict:
        """Load weekly goals from a JSON file."""
        if os.path.exists(self.goals_file):
            try:
                with open(self.goals_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}

    def save_goals(self, goals: Dict) -> None:
        """Save weekly goals to a JSON file."""
        if not isinstance(goals, dict):
            raise ValueError("Goals must be a dictionary")
        
        with open(self.goals_file, 'w') as f:
            json.dump(goals, f, indent=2)

    def set_weekly_goal(self, goal: Dict) -> Dict:
        """Set or update a weekly goal."""
        if not isinstance(goal, dict):
            raise ValueError("Goal must be a dictionary")
        
        required_fields = ['session_goal', 'calorie_goal']
        for field in required_fields:
            if field not in goal:
                raise ValueError(f"Missing required field: {field}")
        
        self.weekly_goal = goal
        self.save_goals(goal)
        return goal

    def get_weekly_goal(self) -> Dict:
        """Get the current weekly goal."""
        return getattr(self, 'weekly_goal', {})

    def get_weekly_progress(self) -> Dict:
        """Calculate current week's workout progress toward the goal."""
        now = datetime.datetime.now()
        start_of_week = now - datetime.timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        
        workouts_this_week = [
            w for w in self.workouts 
            if datetime.datetime.fromisoformat(w['date']).replace(tzinfo=None) >= start_of_week
        ]

        total_sessions = len(workouts_this_week)
        total_calories = sum(w['total_calories'] for w in workouts_this_week)

        goal = self.get_weekly_goal()
        return {
            "sessions_completed": total_sessions,
            "calories_burned": total_calories,
            "session_goal": goal.get("session_goal", 0),
            "calorie_goal": goal.get("calorie_goal", 0),
            "week_start": start_of_week.isoformat(),
            "week_end": (start_of_week + datetime.timedelta(days=6)).isoformat()
        }


# ==========================
# Flask Routes
# ==========================

# Initialize tracker
tracker = WorkoutTracker()

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    """Get all workouts with optional limit."""
    limit = request.args.get('limit', type=int)
    workouts = tracker.get_workouts(limit)
    return jsonify({"success": True, "data": workouts})

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    """Add a new workout."""
    try:
        data = request.get_json()
        
        required_fields = ['type', 'duration_minutes', 'exercises']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "error": f"Missing required field: {field}"}), 400
        
        workout = tracker.add_workout(
            workout_type=data['type'],
            duration=data['duration_minutes'],
            exercises=data['exercises'],
            notes=data.get('notes', ''),
            date=data.get('date')
        )
        
        return jsonify({"success": True, "data": workout}), 201
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Get a specific workout by ID."""
    workout = tracker.get_workout_by_id(workout_id)
    
    if workout:
        return jsonify({"success": True, "data": workout})
    else:
        return jsonify({"success": False, "error": "Workout not found"}), 404

@app.route('/api/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout by ID."""
    success = tracker.delete_workout(workout_id)
    
    if success:
        return jsonify({"success": True, "message": "Workout deleted successfully"})
    else:
        return jsonify({"success": False, "error": "Workout not found"}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get workout statistics."""
    stats = tracker.get_stats()
    return jsonify({"success": True, "data": stats})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

# ==========================
# Reminder Routes
# ==========================

@app.route('/api/reminders', methods=['POST'])
def create_reminder():
    """Add a new workout reminder."""
    try:
        data = request.get_json()
        date = data.get('date')
        message = data.get('message', 'Workout Reminder')

        if not date:
            return jsonify({"success": False, "error": "Missing 'date' field"}), 400

        reminder = tracker.add_reminder(date=date, message=message)
        return jsonify({"success": True, "data": reminder}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reminders', methods=['GET'])
def get_reminders():
    """Get all upcoming reminders."""
    reminders = tracker.get_upcoming_reminders()
    return jsonify({"success": True, "data": reminders})

# ==========================
# Weekly Goals Routes
# ==========================

@app.route('/api/goals', methods=['POST'])
def add_goal():
    try:
        goal_data = request.json
        goal = {
            'id': len(tracker.goals) + 1,
            'type': goal_data['type'],
            'target': goal_data['target'],
            'deadline': goal_data['deadline'],
            'completed': False
        }
        tracker.goals.append(goal)
        tracker.save_goals()
        return jsonify({"success": True, "data": goal}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/goals', methods=['GET'])
def get_weekly_goal():
    """Get current weekly goal."""
    goal = tracker.get_weekly_goal()
    return jsonify({"success": True, "data": goal})

@app.route('/api/goals/progress', methods=['GET'])
def get_weekly_progress():
    """Get progress toward weekly goals."""
    progress = tracker.get_weekly_progress()
    return jsonify({"success": True, "data": progress})

# ==========================
# Run the App
# ==========================

if __name__ == '__main__':
    print("🏋️  Starting Workout Tracker API...")
    print("📊 API will be available at: http://localhost:5000")
    print("🌐 Frontend should connect to: http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000)
