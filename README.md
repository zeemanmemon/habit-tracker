Habit Tracker
=============

_Track habits, build streaks, and earn badges, all from a simple desktop app._

Overview
--------

This is a user-friendly habit tracker built with **Python** and **Tkinter**, inspired by the book [*Atomic Habits* by James Clear](https://jamesclear.com/atomic-habits). It helps you build consistency through:

* 📅 Calendar-based habit tracking
* 🔥 Streak and longest streak tracking
* 🏅 Achievement badges for consistency
* ✏️ Add, rename, or delete habits
* 🔎 Filter by: **All**, **This Week**, or **This Month**
* 👁️ View all badges and how to earn them

All data is stored locally using a JSON file. No setup or database required.

Features
--------

* **Add Habits** – Track anything like exercise, reading, or hydration
* **Mark as Done** – Select a date and click "Mark as Done" to log a habit
* **Calendar View** – Visualize progress with highlighted completion days
* **Streak Tracking** – See your current streak and all-time longest streak
* **Badge System** – Automatically awarded based on your habit streak
* **Filter Progress** – View activity for all time, this week, or this month
* **Lightweight & Offline** – Works out of the box without internet

Badge Tiers
-----------

| Badge | Requirement |
| --- | --- |
| 🐣 Getting Started | 1-day streak |
| 🌱 Small Streak | 3-day streak |
| 🔥 One Week Warrior | 7-day streak |
| 💪 Consistency Champ | 14-day streak |
| 🏆 Habit Hero | 30-day streak |

Project Structure
-----------------

    
    habit-tracker/
    ├── main.py            → Entry point
    ├── tracker_gui.py     → Tkinter GUI logic
    ├── tracker_logic.py   → Data handling and habit logic
    ├── data.json          → Habit tracking storage
    └── README.md          → Project documentation
    

Requirements
------------

* Python 3.7 or higher
* tkinter (comes with Python)
* tkcalendar

Install `tkcalendar` by running:

    pip install tkcalendar

How to Run
----------

1.  Open a terminal in the project directory
2.  Run the app with:

    python main.py

Ideas for Future Features
-------------------------

* 🌙 Dark mode toggle
* 📊 Progress graphs with matplotlib
* 📤 Export data to CSV
* 📝 Add notes for each day
* 🔔 Optional reminders

You're welcome to customize, fork, or expand this project to suit your needs.
