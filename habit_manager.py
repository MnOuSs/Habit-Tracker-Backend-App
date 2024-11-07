import datetime
from datetime import date, datetime, timedelta

class HabitManager:
    """
    Manages a list of habits, including adding, completing, editing, and deleting habits, as well as
    managing streaks based on the completion dates and periodicity of each habit.
    """

    def __init__(self, storage):
        """
        Initialize HabitManager with data storage.

        Args:
            storage (DataStorage): Storage object to persist habits.
        """
        self.habits = []
        self.storage = storage

    def add_habit(self, habit):
        """
        Add a new habit to the manager.

        Args:
            habit (Habit): Habit to add.
        """
        self.habits.append(habit)

    def complete_habit(self, habit_name):
        """
        Mark a habit as complete for the current period, if it hasn’t already been marked.

        Args:
            habit_name (str): The name of the habit to complete.

        Returns:
            bool: True if the habit was successfully completed for the period, False if it was
            already completed or not found.
        """
        today = datetime.now().date()
        habit = self.get_habit(habit_name)
        if habit:
            last_completion = max(habit.completion_dates) if habit.completion_dates else None
            if last_completion:
                if habit.periodicity == "daily":
                    period_length = timedelta(days=1)
                elif habit.periodicity == "weekly":
                    period_length = timedelta(weeks=1)
                elif habit.periodicity == "monthly":
                    period_length = timedelta(days=30)

                if today <= last_completion + period_length:
                    print("Habit already completed for this period.")
                    return False

            habit.completion_dates.append(today)
            self.storage.save_habit(habit)
            return True
        return False

    def get_habit(self, name):
        """
        Retrieve a habit by name, case-insensitive.

        Args:
            name (str): The name of the habit to retrieve.

        Returns:
            Habit or None: The habit object if found, or None if not found.
        """
        name = name.lower()
        for habit in self.habits:
            if habit.name.lower() == name:
                return habit
        return None

    def edit_habit(self, name, new_name=None, new_description=None, new_periodicity=None):
        """
        Edit an existing habit's details, updating name, description, or periodicity as provided.

        Args:
            name (str): The current name of the habit.
            new_name (str, optional): The new name for the habit.
            new_description (str, optional): The new description for the habit.
            new_periodicity (str, optional): The new periodicity for the habit.

        Returns:
            bool: True if the habit was found and updated, False otherwise.
        """
        habit = self.get_habit(name)
        if not habit:
            print("Habit does not exist.")
            return False

        if new_name:
            habit.name = new_name
        if new_description:
            habit.description = new_description
        if new_periodicity:
            habit.periodicity = new_periodicity
        self.storage.save_habit(habit)
        return True

    def check_streak(self, habit):
        """
        Calculate the current streak for a habit by checking consecutive completions within each period.

        Args:
            habit (Habit): The habit object for which to calculate the streak.

        Returns:
            int: The current streak count.
        """
        today = date.today()
        streak = 0
        current_period_start = today

        if habit.periodicity == "daily":
            period_length = timedelta(days=1)
        elif habit.periodicity == "weekly":
            period_length = timedelta(weeks=1)
        elif habit.periodicity == "monthly":
            period_length = timedelta(days=30)

        for completion_date in sorted(habit.completion_dates, reverse=True):
            if completion_date >= current_period_start - period_length:
                streak += 1
                current_period_start -= period_length
            else:
                break
        return streak

    def delete_habit(self, name):
        """
        Delete a habit by name.

        Args:
            name (str): Name of the habit to delete.

        Returns:
            bool: True if the habit was found and deleted, False otherwise.
        """
        for habit in self.habits:
            if habit.name == name.lower():
                self.habits.remove(habit)
                return True
        return False

    def get_habits(self):
        """
        Retrieve the list of all managed habits.

        Returns:
            list: List of Habit objects.
        """
        return self.habits
