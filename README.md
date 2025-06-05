# 🏋️ Workout Tracker

A full-stack fitness tracking application that allows users to log, view, and analyze their workouts. The project consists of a Flask-based REST API backend and a modern, responsive HTML/JavaScript frontend.

---

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Backend API](#backend-api)
- [Frontend Usage](#frontend-usage)
- [Data Format](#data-format)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features
- Add detailed workout sessions with multiple exercises
- Track workout type, duration, notes, and calories burned
- View, filter, and delete past workouts
- Visualize workout statistics (totals, averages, last 30 days, types)
- Responsive, modern UI with smooth navigation
- Persistent data storage in JSON file

---


### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd workout-tracker
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. **Start the backend server:**
   ```bash
   python apis.py
   ```
   The API will be available at [http://localhost:5000](http://localhost:5000)

2. **Open the frontend:**
   - Open `front.html` in your web browser.
   - The frontend will connect to the backend API at `http://localhost:5000/api`.

---

## Backend API

The backend is a Flask REST API. Main endpoints:

### Health Check
- `GET /api/health` — Returns API status.

### Workouts
- `GET /api/workouts?limit=<n>` — List all workouts (optionally limit results)
- `POST /api/workouts` — Add a new workout
- `GET /api/workouts/<id>` — Get a specific workout by ID
- `DELETE /api/workouts/<id>` — Delete a workout by ID

#### Example: Add Workout
```json
POST /api/workouts
{
  "type": "strength",
  "duration_minutes": 60,
  "exercises": [
    {"name": "Bench Press", "type": "strength", "sets": 4, "reps": 8, "weight_kg": 60},
    {"name": "Running", "type": "cardio", "distance_km": 5}
  ],
  "notes": "Felt strong today!"
}
```

### Statistics
- `GET /api/stats` — Returns workout stats (totals, averages, last 30 days, types)

---

## Frontend Usage
- **Add Workout:** Fill out the form, add exercises, and save.
- **View Workouts:** Browse, filter, and delete past workouts.
- **Statistics:** See totals, averages, and breakdowns by type.

---

## Data Format

Workouts are stored in `workouts.json` (auto-created). Example entry:
```json
{
  "id": 1,
  "date": "2024-06-01T10:00:00",
  "type": "strength",
  "duration_minutes": 60,
  "exercises": [
    {"name": "Bench Press", "type": "strength", "sets": 4, "reps": 8, "weight_kg": 60},
    {"name": "Running", "type": "cardio", "distance_km": 5}
  ],
  "notes": "Felt strong today!",
  "total_calories": 390
}
```

---

## Troubleshooting
- **Cannot connect to backend:** Ensure you started the Flask server (`python apis.py`).
- **CORS errors:** The backend enables CORS for local development. If you change ports, update `API_BASE` in `front.html`.
- **Data not saving:** Check for write permissions in the project directory.
- **Port in use:** Change the port in `apis.py` if 5000 is occupied.

