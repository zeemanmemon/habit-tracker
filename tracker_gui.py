import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tracker_logic import (
    add_habit,
    mark_habit_on_date,
    get_habits,
    delete_habit,
    rename_habit,
)
from datetime import datetime
from tkcalendar import Calendar


class HabitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")

        # Entry for adding a habit
        self.habit_entry = tk.Entry(root, width=30)
        self.habit_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to add habit
        self.add_btn = tk.Button(root, text="Add Habit", command=self.add_habit)
        self.add_btn.grid(row=0, column=1, padx=5)

        # Button to mark habit as done
        self.mark_btn = tk.Button(root, text="Mark as Done", command=self.mark_done)
        self.mark_btn.grid(row=1, column=1, padx=5)

        # Button to delete habit
        self.delete_btn = tk.Button(root, text="Delete Habit", command=self.delete_habit)
        self.delete_btn.grid(row=2, column=1, padx=5)

        # Button to rename habit
        self.rename_btn = tk.Button(root, text="Rename Habit", command=self.rename_habit_prompt)
        self.rename_btn.grid(row=3, column=1, padx=5)

        # Button to view all badges
        self.view_badges_btn = tk.Button(root, text="View All Badges", command=self.view_all_badges)
        self.view_badges_btn.grid(row=4, column=1, padx=5)

        # Habit list display
        self.habits_listbox = tk.Listbox(root, width=50)
        self.habits_listbox.grid(row=1, column=0, rowspan=5, padx=10, pady=10)
        self.habits_listbox.bind("<<ListboxSelect>>", self.show_calendar_for_habit)

        # Label to display streak + badge
        self.streak_label = tk.Label(root, text="Streak: 0 days | 🐣 Getting Started", font=('Arial', 12, 'bold'))
        self.streak_label.grid(row=6, column=0, pady=(5, 0))

        # Filter dropdown
        self.filter_var = tk.StringVar(value="All")
        self.filter_dropdown = ttk.Combobox(
            root,
            textvariable=self.filter_var,
            values=["All", "This Week", "This Month"],
            state="readonly",
            width=20
        )
        self.filter_dropdown.grid(row=6, column=1, padx=10, pady=5)
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.show_calendar_for_habit)

        # Calendar widget
        self.calendar = Calendar(root, selectmode='day')
        self.calendar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.refresh_habits()

    def add_habit(self):
        habit_name = self.habit_entry.get().strip()
        if habit_name:
            add_habit(habit_name)
            self.refresh_habits()
            self.habit_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a habit name.")

    def mark_done(self):
        selected = self.habits_listbox.curselection()
        if selected:
            habit = self.habits_listbox.get(selected)
            selected_date = self.calendar.selection_get()

            if selected_date is None:
                messagebox.showwarning("No Date Selected", "Please select a date from the calendar.")
                return

            date_str = selected_date.strftime("%Y-%m-%d")
            mark_habit_on_date(habit, date_str)
            messagebox.showinfo("Success", f"Marked '{habit}' as done on {date_str}")
            self.show_calendar_for_habit()
        else:
            messagebox.showwarning("Selection Error", "Please select a habit.")

    def delete_habit(self):
        selected = self.habits_listbox.curselection()
        if selected:
            habit = self.habits_listbox.get(selected)
            confirm = messagebox.askyesno("Delete Habit", f"Are you sure you want to delete '{habit}'?")
            if confirm:
                delete_habit(habit)
                self.refresh_habits()
                messagebox.showinfo("Deleted", f"Habit '{habit}' has been deleted.")
        else:
            messagebox.showwarning("Selection Error", "Please select a habit to delete.")

    def rename_habit_prompt(self):
        selected = self.habits_listbox.curselection()
        if selected:
            old_name = self.habits_listbox.get(selected)
            new_name = simpledialog.askstring("Rename Habit", f"Rename '{old_name}' to:")
            if new_name:
                success = rename_habit(old_name, new_name.strip())
                if success:
                    messagebox.showinfo("Renamed", f"'{old_name}' renamed to '{new_name.strip()}'")
                    self.refresh_habits()
                else:
                    messagebox.showwarning("Rename Error", "Rename failed. Name might already exist.")
        else:
            messagebox.showwarning("Selection Error", "Please select a habit to rename.")

    def refresh_habits(self):
        self.habits_listbox.delete(0, tk.END)
        data = get_habits()
        for habit in data:
            self.habits_listbox.insert(tk.END, habit)
        self.clear_calendar()
        self.streak_label.config(text="Streak: 0 days | 🐣 Getting Started")

    def clear_calendar(self):
        self.calendar.calevent_remove('all')

    def calculate_streaks(self, dates):
        if not dates:
            return 0, 0

        date_objs = sorted([datetime.strptime(d, "%Y-%m-%d").date() for d in dates])
        streaks = []
        current_streak = 1
        longest_streak = 1

        for i in range(1, len(date_objs)):
            diff = (date_objs[i] - date_objs[i - 1]).days
            if diff == 1:
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1

        streaks.append(current_streak)
        longest_streak = max(streaks)

        today = datetime.today().date()
        if date_objs[-1] == today:
            return streaks[-1], longest_streak
        else:
            return 0, longest_streak

    def get_streak_badge(self, streak):
        if streak >= 30:
            return "🏆 Habit Hero"
        elif streak >= 14:
            return "💪 Consistency Champ"
        elif streak >= 7:
            return "🔥 One Week Warrior"
        elif streak >= 3:
            return "🌱 Small Streak"
        elif streak >= 1:
            return "🐣 Getting Started"
        else:
            return "None"

    def show_calendar_for_habit(self, event=None):
        selected = self.habits_listbox.curselection()
        if selected:
            habit = self.habits_listbox.get(selected)
            data = get_habits()
            dates = data[habit]["dates"]
            self.clear_calendar()

            filter_option = self.filter_var.get()
            today = datetime.today().date()

            for d in dates:
                try:
                    date_obj = datetime.strptime(d, "%Y-%m-%d").date()

                    if filter_option == "This Week" and (today - date_obj).days > 6:
                        continue
                    elif filter_option == "This Month" and (today.month != date_obj.month or today.year != date_obj.year):
                        continue

                    self.calendar.calevent_create(date_obj, 'Done', 'done')
                except ValueError:
                    continue

            self.calendar.tag_config('done', background='green', foreground='white')

            current_streak, longest_streak = self.calculate_streaks(dates)
            badge = self.get_streak_badge(current_streak)

            self.streak_label.config(
                text=f"Streak: {current_streak} day{'s' if current_streak != 1 else ''} "
                     f"(Longest: {longest_streak}) | {badge}"
            )

    def view_all_badges(self):
        badge_window = tk.Toplevel(self.root)
        badge_window.title("Badge Tiers")
        badge_window.geometry("320x220")

        badge_info = [
            ("🐣 Getting Started", "1-day streak"),
            ("🌱 Small Streak", "3-day streak"),
            ("🔥 One Week Warrior", "7-day streak"),
            ("💪 Consistency Champ", "14-day streak"),
            ("🏆 Habit Hero", "30-day streak"),
        ]

        tk.Label(badge_window, text="🏅 Achievement Badges", font=('Arial', 14, 'bold')).pack(pady=10)

        for name, condition in badge_info:
            tk.Label(badge_window, text=f"{name}: {condition}", font=('Arial', 11)).pack(anchor="w", padx=20)

        tk.Button(badge_window, text="Close", command=badge_window.destroy).pack(pady=10)


def start_gui():
    root = tk.Tk()
    app = HabitTrackerApp(root)
    root.mainloop()
