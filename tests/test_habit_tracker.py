import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from habit import Habit
from habit_manager import HabitManager
from data_storage import DataStorage
from habit_analyzer import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak,
    get_longest_streak_for_habit
)
from datetime import datetime, timedelta

class TestHabitManager(unittest.TestCase):
    """
    Unit tests for HabitManager functionalities, including habit creation, editing, and deletion.
    """

    def setUp(self):
        """
        Set up an in-memory database and initialize HabitManager with a sample habit for testing.
        """
        self.data_storage = DataStorage(":memory:")
        self.habit_manager = HabitManager(self.data_storage)
        self.sample_habit = Habit(
            name="exercise",
            description="Daily exercise habit",
            periodicity="daily",
            completion_dates=[datetime.now().date() - timedelta(days=i) for i in range(5)]
        )
        self.habit_manager.add_habit(self.sample_habit)
        self.data_storage.save_habit(self.sample_habit)

    def test_create_habit(self):
        """
        Test the creation of a new habit and ensure it is added to the habit manager.
        """
        new_habit = Habit(name="reading", description="Reading daily", periodicity="daily")
        self.habit_manager.add_habit(new_habit)
        self.data_storage.save_habit(new_habit)
        loaded_habits = self.habit_manager.habits
        self.assertIn(new_habit, loaded_habits, "New habit should be in the habit list after creation")

    def test_edit_habit(self):
        """
        Test editing a habit's name and periodicity, verifying the changes are saved.
        """
        self.habit_manager.edit_habit(name="exercise", new_name="workout", new_periodicity="weekly")
        edited_habit = self.habit_manager.get_habit("workout")
        self.assertIsNotNone(edited_habit, "Edited habit should be retrievable by the new name")
        self.assertEqual(edited_habit.periodicity, "weekly", "Habit periodicity should be updated to weekly")

    def test_delete_habit(self):
        """
        Test deletion of a habit and ensure it is removed from the habit manager and database.
        """
        self.habit_manager.delete_habit("exercise")
        self.data_storage.delete_habit("exercise")
        deleted_habit = self.habit_manager.get_habit("exercise")
        self.assertIsNone(deleted_habit, "Habit should not exist after deletion")

    def tearDown(self):
        """
        Clean up resources by closing the in-memory database after each test.
        """
        self.data_storage.close()

class TestHabitAnalytics(unittest.TestCase):
    """
    Unit tests for habit analytics, including retrieval of habits, filtering by periodicity,
    and calculating longest streaks.
    """

    def setUp(self):
        """
        Set up in-memory DataStorage and HabitManager with sample habits for testing analytics.
        """
        self.data_storage = DataStorage(":memory:")
        self.habit_manager = HabitManager(self.data_storage)
        self.daily_habit = Habit(
            name="meditate",
            description="Daily meditation",
            periodicity="daily",
            completion_dates=[datetime.now().date() - timedelta(days=i) for i in range(5)]
        )
        self.weekly_habit = Habit(
            name="meeting",
            description="Weekly meeting",
            periodicity="weekly",
            completion_dates=[datetime.now().date() - timedelta(weeks=i) for i in range(3)]
        )
        self.monthly_habit = Habit(
            name="budget",
            description="Monthly budget review",
            periodicity="monthly",
            completion_dates=[datetime.now().date() - timedelta(days=30 * i) for i in range(4)]
        )
        for habit in [self.daily_habit, self.weekly_habit, self.monthly_habit]:
            self.habit_manager.add_habit(habit)
            self.data_storage.save_habit(habit)

    def test_get_all_habits(self):
        """
        Test retrieval of all habits from HabitManager.
        """
        all_habits = get_all_habits(self.habit_manager)
        self.assertEqual(len(all_habits), 3, "Expected to retrieve all habits")
        self.assertIn(self.daily_habit, all_habits, "Daily habit should be present in all habits")

    def test_get_habits_by_periodicity(self):
        """
        Test filtering of habits by periodicity to ensure correct filtering.
        """
        weekly_habits = get_habits_by_periodicity(self.habit_manager, "weekly")
        self.assertEqual(len(weekly_habits), 1, "Expected one weekly habit")
        self.assertIn(self.weekly_habit, weekly_habits, "Weekly habit should be in the filtered list")

    def test_get_longest_streak(self):
        """
        Test calculation of the longest streak across all habits.
        """
        longest_streak, periodicity = get_longest_streak(self.habit_manager.habits)
        self.assertEqual(longest_streak, 4, "Expected longest streak to be 4")
        self.assertEqual(periodicity, "monthly", "Expected longest streak periodicity to be monthly")

    def test_get_longest_streak_for_habit(self):
        """
        Test calculation of the longest streak for a specific habit.
        """
        streak, periodicity = get_longest_streak_for_habit(self.daily_habit)
        self.assertEqual(streak, 5, "Expected daily habit streak to be 5")
        self.assertEqual(periodicity, "daily", "Expected periodicity for streak to match the habit's periodicity")

    def tearDown(self):
        """
        Clean up resources by closing the in-memory database after each test.
        """
        self.data_storage.close()

if __name__ == "__main__":
    unittest.main()
