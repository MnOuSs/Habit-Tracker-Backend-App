import random
from habit import Habit
from data_storage import DataStorage
from datetime import datetime, timedelta
import calendar

data_storage_instance = DataStorage(db_name="habits.db")

def generate_random_dates(periodicity, min_dates=4, max_dates=10):
    """
    Generate random consecutive dates based on the periodicity to create varied streak lengths.

    Args:
        periodicity (str): The frequency of the habit ('daily', 'weekly', or 'monthly').
        min_dates (int): Minimum number of dates to generate.
        max_dates (int): Maximum number of dates to generate.

    Returns:
        list: A list of dates sorted in descending order, based on the specified periodicity.
    """
    num_dates = random.randint(min_dates, max_dates)
    dates = []
    today = datetime.now().date()

    if periodicity == "daily":
        dates = [today - timedelta(days=i) for i in range(num_dates)]

    elif periodicity == "weekly":
        dates = [today - timedelta(weeks=i) for i in range(num_dates)]

    elif periodicity == "monthly":
        for i in range(num_dates):
            month = today.month - i
            year = today.year
            while month <= 0:
                month += 12
                year -= 1
            last_day_of_month = calendar.monthrange(year, month)[1]
            day = min(today.day, last_day_of_month)
            dates.append(datetime(year, month, day).date())

    return sorted(dates, reverse=True)

def load_predefined_habits():
    """
    Define and load a set of predefined habits with randomly generated completion dates.

    Returns:
        list: A list of Habit objects with predefined attributes and randomly generated completion dates.
    """
    habits = [
        Habit(name="exercise", description="Exercise daily", periodicity="daily", completion_dates=generate_random_dates("daily")),
        Habit(name="read", description="Read daily", periodicity="daily", completion_dates=generate_random_dates("daily")),
        Habit(name="meeting", description="Attend weekly meeting", periodicity="weekly", completion_dates=generate_random_dates("weekly")),
        Habit(name="clean", description="Weekly house cleaning", periodicity="weekly", completion_dates=generate_random_dates("weekly")),
        Habit(name="budget", description="Review monthly budget", periodicity="monthly", completion_dates=generate_random_dates("monthly")),
        Habit(name="maintenance", description="Monthly car maintenance", periodicity="monthly", completion_dates=generate_random_dates("monthly")),
    ]
    for habit in habits:
        print(f"{habit.name.capitalize()} Streak:", habit.streak)
    return habits

def initialize_habits(data_storage):
    """
    Load predefined habits into the database, updating them if they already exist.

    Args:
        data_storage (DataStorage): The storage instance used to save and retrieve habits.
    """
    predefined_habits = load_predefined_habits()
    existing_habits = {habit.name: habit for habit in data_storage.load_habits()}

    for habit in predefined_habits:
        if habit.name in existing_habits:
            data_storage.save_habit(habit)
        else:
            data_storage.save_habit(habit)

    print("Predefined habits have been loaded or updated in the database.")

if __name__ == "__main__":
    initialize_habits(data_storage_instance)
