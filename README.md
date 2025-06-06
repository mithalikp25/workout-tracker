

# 🏋️‍♀️ **Workout Tracker**

A full-stack fitness tracking application built with **Flask (Backend)** and **HTML/CSS/JavaScript (Frontend)** that allows users to **log, track, and visualize** their fitness journey with powerful features and a modern UI.

---

## 📑 Table of Contents

* [✨ Features](#-features)
* [🖼️ Screenshots](#️-screenshots)
* [🚀 Getting Started](#-getting-started)
* [📡 Backend API](#-backend-api)
* [💻 Frontend Usage](#-frontend-usage)
* [📁 Data Format](#-data-format)
* [🛠️ Troubleshooting](#-troubleshooting)
* [📄 License](#-license)

---

## ✨ Features

✅ Add and manage detailed workout sessions
✅ Multiple exercise types: **Strength**, **Cardio**, etc.
✅ Track workout **type**, **duration**, **notes**, and **calories burned**
✅ Interactive **Calendar View** (Month/Week) with indicators
✅ In-app **Stopwatch** ⏱️ for live timing
✅ **Weekly Goals** setup and progress tracker 📈
✅ **Workout Reminders** with alerts ⏰
✅ Total **Time Recorder** for weekly/monthly summaries
✅ Clean **UI subtitles**, intuitive navigation, and responsive layout
✅ Personalized **logo** for branding
✅ Visualize stats: **totals**, **averages**, **workout types**, **last 30 days**
✅ Persistent data storage using a **JSON file**

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.7 or higher
* `pip` (Python package manager)

### 📥 Installation

```bash
# 1. Clone the repository
git clone <repo-url>
cd workout-tracker

# 2. Install Python dependencies
pip install -r requirements.txt
```

### ▶️ Running the Application

**Start the backend server:**

```bash
python apis.py
```

➡️ API will run at: `http://localhost:5000`

**Open the frontend:**

* Double-click or open `front.html` in your browser.
* It connects to `http://localhost:5000/api`.

---

## 📡 Backend API

Built with **Flask** and returns JSON responses.

### ✅ Health Check

```
GET /api/health
```

### 🏋️ Workouts

* `GET /api/workouts?limit=n` — Fetch workouts
* `POST /api/workouts` — Add a new workout
* `GET /api/workouts/<id>` — Get workout by ID
* `DELETE /api/workouts/<id>` — Delete workout

#### 📝 Example: Add Workout

```json
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

### 📊 Stats

```
GET /api/stats
```

Returns summary of workouts (averages, types, duration, calories, etc.)

---

## 💻 Frontend Usage

* ➕ **Add Workout** – via form interface
* 📅 **Calendar View** – switch between Month and Week
* ⏱️ **Stopwatch** – track live workout duration
* 🎯 **Set Weekly Goals** – and monitor them
* 🧠 **Smart Reminders** – don't miss a workout
* 📈 **View Statistics** – by type, duration, and trends

---

## 📁 Data Format

Stored in `workouts.json`. Example:

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

## 🛠️ Troubleshooting

| Issue                       | Solution                                                             |
| --------------------------- | -------------------------------------------------------------------- |
| ❌ Cannot connect to backend | Make sure Flask server is running (`python apis.py`)                 |
| ⚠️ CORS errors              | Check ports and make sure API\_BASE in frontend matches backend port |
| 💾 Data not saving          | Ensure write permissions for `workouts.json` file                    |
| 🛑 Port 5000 already in use | Change the port in `apis.py` and frontend API endpoint accordingly   |

---