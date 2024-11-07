from datetime import datetime, timedelta

class Habit:
    """A class representing a habit with a name, description, periodicity, and a completion history."""

    def __init__(self, name, description, periodicity, completion_dates=None):
        """
        Initialize a Habit instance.

        Args:
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (str): The interval of the habit ('daily', 'weekly', or 'monthly').
            completion_dates (list): A list of dates when the habit was completed.
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.completion_dates = sorted(completion_dates or [])

    @property
    def streak(self):
        """Calculate the current streak based on consecutive completion dates."""
        return self.calculate_streak()

    def calculate_streak(self):
        """
        Calculate the current streak of consecutive completions.

        Returns:
            int: The current streak count.
        """
        if not self.completion_dates:
            return 0

        sorted_dates = sorted(self.completion_dates, reverse=True)
        streak = 1
        current_date = sorted_dates[0]

        for next_date in sorted_dates[1:]:
            if self._is_consecutive(current_date, next_date):
                streak += 1
                current_date = next_date
            else:
                break

        return streak

    def _is_consecutive(self, date1, date2):
        """
        Check if two dates are consecutive based on the habit's periodicity.

        Args:
            date1 (date): The later date in the sequence.
            date2 (date): The earlier date in the sequence.

        Returns:
            bool: True if the dates are consecutive, False otherwise.
        """
        if self.periodicity == "daily":
            return date1 - date2 == timedelta(days=1)
        elif self.periodicity == "weekly":
            return date1 - date2 == timedelta(weeks=1)
        elif self.periodicity == "monthly":
            return (date1.month - date2.month == 1 and date1.year == date2.year) or \
                   (date1.month == 1 and date2.month == 12 and date1.year - date2.year == 1)
        return False

    def __repr__(self):
        """
        Return a string representation of the Habit instance, including its name, periodicity, and current streak.

        Returns:
            str: String representation of the Habit instance.
        """
        return f"Habit(name={self.name}, periodicity={self.periodicity}, streak={self.streak})"
