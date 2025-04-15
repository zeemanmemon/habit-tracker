import json
from datetime import date

DATA_FILE = 'data.json'

def load_data():
    """Load habit data from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {}

def save_data(data):
    """Save habit data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def add_habit(habit_name):
    """Add a new habit if it doesn't already exist."""
    data = load_data()
    if habit_name not in data:
        data[habit_name] = {"dates": []}
        save_data(data)

def mark_habit(habit_name):
    """Mark the habit as completed for today."""
    data = load_data()
    today = str(date.today())
    if habit_name in data and today not in data[habit_name]["dates"]:
        data[habit_name]["dates"].append(today)
        save_data(data)

def get_habits():
    """Return all habits and their completed dates."""
    return load_data()

def delete_habit(habit_name):
    data = load_data()
    if habit_name in data:
        del data[habit_name]
        save_data(data)

def rename_habit(old_name, new_name):
    data = load_data()
    if old_name in data and new_name not in data:
        data[new_name] = data.pop(old_name)
        save_data(data)
        return True
    return False

def mark_habit_on_date(habit_name, date_str):
    data = load_data()
    if habit_name in data and date_str not in data[habit_name]["dates"]:
        data[habit_name]["dates"].append(date_str)
        save_data(data)
