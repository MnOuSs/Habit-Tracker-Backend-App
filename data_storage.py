import sqlite3
from datetime import datetime
from habit import Habit

class DataStorage:
    """
    A class to handle data storage for habits, using an SQLite database to save, load, and delete habits.
    """

    def __init__(self, db_name="habits.db"):
        """
        Initialize the DataStorage instance with a database connection and cursor, creating the habits table if needed.

        Args:
            db_name (str): Name of the SQLite database file. Defaults to 'habits.db'.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_habits_table()

    def _create_habits_table(self):
        """
        Create the habits table in the database if it does not already exist.
        The table includes columns for id, name, description, periodicity, and completion_dates.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                periodicity TEXT NOT NULL,
                completion_dates TEXT
            )
        ''')
        self.connection.commit()

    def save_habit(self, habit):
        """
        Save a habit to the database, updating it if it already exists.

        Args:
            habit (Habit): The Habit object to save, including its name, description, periodicity, and completion dates.
        """
        completion_dates = ",".join(date.strftime('%Y-%m-%d') for date in habit.completion_dates) if habit.completion_dates else ""
        self.cursor.execute('''
            INSERT OR REPLACE INTO habits (name, description, periodicity, completion_dates)
            VALUES (?, ?, ?, ?)
        ''', (habit.name, habit.description, habit.periodicity, completion_dates))
        self.connection.commit()

    def delete_habit(self, habit_name):
        """
        Delete a habit from the database by its name.

        Args:
            habit_name (str): The name of the habit to delete.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))
        self.connection.commit()

    def load_habits(self):
        """
        Load all habits from the database, converting them to Habit objects.

        Returns:
            list: A list of Habit objects, each representing a habit stored in the database.
        """
        self.cursor.execute('SELECT name, description, periodicity, completion_dates FROM habits')
        rows = self.cursor.fetchall()
        habits = []
        for row in rows:
            name, description, periodicity, completion_dates = row
            completion_dates_list = [datetime.strptime(date, '%Y-%m-%d').date() for date in completion_dates.split(",") if date]
            habit = Habit(name, description, periodicity, completion_dates_list)
            habits.append(habit)
        return habits

    def close(self):
        """
        Close the database connection if it is open.
        """
        if self.connection:
            self.connection.close()
