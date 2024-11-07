def get_all_habits(tracker):
    """
    Retrieve all habits from the habit manager.

    Args:
        tracker (HabitManager): The habit manager instance.

    Returns:
        list: List of all Habit objects managed by the tracker.
    """
    return tracker.get_habits()

def get_habits_by_periodicity(tracker, periodicity):
    """
    Filter habits by specified periodicity.

    Args:
        tracker (HabitManager): The habit manager instance.
        periodicity (str): Desired periodicity ('daily', 'weekly', or 'monthly').

    Returns:
        list: List of Habit objects with the specified periodicity.
    """
    return [habit for habit in tracker.get_habits() if habit.periodicity == periodicity]

def get_longest_streak(habits):
    """
    Determine the longest streak across all habits, converting the streak count to days for comparison.

    Args:
        habits (list): List of Habit objects to evaluate.

    Returns:
        tuple: The longest streak (int) and its periodicity (str).
    """
    longest_streak = 0
    longest_periodicity = None

    for habit in habits:
        streak = habit.streak
        periodicity = habit.periodicity

        if periodicity == "daily":
            streak_in_days = streak
        elif periodicity == "weekly":
            streak_in_days = streak * 7
        elif periodicity == "monthly":
            streak_in_days = streak * 30
        else:
            continue

        if streak_in_days > longest_streak:
            longest_streak = streak_in_days
            longest_periodicity = periodicity

    if longest_periodicity is None:
        return 0, "period"

    if longest_periodicity == "daily":
        display_streak = longest_streak
    elif longest_periodicity == "weekly":
        display_streak = longest_streak // 7
    elif longest_periodicity == "monthly":
        display_streak = longest_streak // 30

    return display_streak, longest_periodicity

def get_longest_streak_for_habit(habit):
    """
    Retrieve the longest streak and periodicity for a specific habit.

    Args:
        habit (Habit): The habit object to evaluate.

    Returns:
        tuple: Longest streak count (int) and periodicity (str).
    """
    return habit.streak, habit.periodicity
