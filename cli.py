import click
from habit_manager import HabitManager
from habit import Habit
from data_storage import DataStorage
from habit_analyzer import get_all_habits, get_habits_by_periodicity, get_longest_streak, get_longest_streak_for_habit

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
RESET = "\033[0m"

tracker = HabitManager(DataStorage())
tracker.habits = tracker.storage.load_habits()

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """
    Command-line interface for managing habits.

    Provides commands for creating, completing, deleting, listing, and analyzing habits.
    If invoked without a command, an interactive menu is displayed.
    """
    if ctx.invoked_subcommand is None:
        interactive_menu()

@click.command()
@click.argument('name')
@click.argument('description')
@click.argument('periodicity')
def create_habit(name, description, periodicity):
    """
    Create a new habit with a specified name, description, and periodicity.

    Args:
        name (str): Name of the habit.
        description (str): Description of the habit.
        periodicity (str): Frequency of the habit ('daily', 'weekly', or 'monthly').
    """
    if periodicity.lower() not in ["daily", "weekly", "monthly"]:
        click.echo(f"{CYAN}Invalid periodicity. Please choose 'daily', 'weekly', or 'monthly'.{RESET}")
        return
    habit = Habit(name.lower(), description, periodicity.lower())
    tracker.add_habit(habit)
    tracker.storage.save_habit(habit)
    click.echo(f"{CYAN}The habit '{name.lower()}' has been created with a {periodicity} periodicity.{RESET}")

@click.command()
@click.argument('habit_name')
def complete_habit(habit_name):
    """
    Mark a habit as complete and update the streak.

    Args:
        habit_name (str): The name of the habit to complete.
    """
    if tracker.complete_habit(habit_name):
        habit = next((h for h in tracker.habits if h.name == habit_name.lower()), None)
        if habit:
            streak = tracker.check_streak(habit)
            unit = {"daily": "day", "weekly": "week", "monthly": "month"}.get(habit.periodicity, "period")
            if streak > 0:
                click.echo(
                    f"{CYAN}Congratulations! You've maintained your streak of {streak} {unit}(s) for the habit '{habit_name.lower()}'.{RESET}")
            else:
                click.echo(
                    f"{CYAN}The habit '{habit_name.lower()}' was broken. Start building the streak again!{RESET}")
    else:
        click.echo(f"{CYAN}The habit '{habit_name.lower()}' has already been completed for this period.{RESET}")

@click.command()
@click.argument('name')
def edit_habit(name):
    """
    Edit an existing habit's details, including name, description, and periodicity.

    Args:
        name (str): The name of the habit to edit.
    """
    habit = tracker.get_habit(name.lower())
    if not habit:
        click.echo(f"{RED}Habit '{name}' does not exist.{RESET}")
        return

    new_name = input("Enter new name (or press Enter to keep current): ")
    new_description = input("Enter new description (or press Enter to keep current): ")
    new_periodicity = input("Enter new periodicity (or press Enter to keep current): ")

    tracker.edit_habit(
        name,
        new_name if new_name else None,
        new_description if new_description else None,
        new_periodicity if new_periodicity else None
    )
    click.echo(f"{GREEN}Habit '{name}' updated successfully.{RESET}")

@click.command()
@click.argument('habit_name')
def delete_habit(habit_name):
    """
    Delete a habit from the tracker and database by name.

    Args:
        habit_name (str): The name of the habit to delete.
    """
    success = tracker.delete_habit(habit_name.lower())
    if success:
        tracker.storage.delete_habit(habit_name.lower())
        click.echo(f"{CYAN}The habit '{habit_name.lower()}' has been deleted.{RESET}")
    else:
        click.echo(f"{CYAN}The habit '{habit_name.lower()}' cannot be found.{RESET}")

@click.command()
def list_all_habits():
    """
    List all habits currently tracked, displaying their name, periodicity, streak, and description.
    """
    habits = get_all_habits(tracker)
    click.echo(f"{GREEN}____________________________________________________{RESET}")
    click.echo("\nAll Tracked Habits:")
    for habit in habits:
        click.echo(f"{RED}--->{RESET} Habit: {CYAN}{habit.name.capitalize()}{RESET}")
        click.echo(f"     Periodicity: {CYAN}{habit.periodicity.capitalize()}{RESET}")
        click.echo(f"     Description: {CYAN}{habit.description.capitalize()}{RESET}")
    click.echo(f"{GREEN}____________________________________________________{RESET}")

@click.command()
@click.argument('periodicity')
def list_habits_by_periodicity(periodicity):
    """
    List habits by specified periodicity (daily, weekly, or monthly).

    Args:
        periodicity (str): The periodicity filter for the list ('daily', 'weekly', or 'monthly').
    """
    if periodicity.lower() not in ["daily", "weekly", "monthly"]:
        click.echo(f"{CYAN}Invalid periodicity. Please choose 'daily', 'weekly', or 'monthly'.{RESET}")
        return
    habits = get_habits_by_periodicity(tracker, periodicity.lower())
    click.echo(f"{CYAN}\nHabits with {periodicity} periodicity:{RESET}")
    for habit in habits:
        click.echo(f"{CYAN}- {habit.name.capitalize()}: Streak - {habit.streak}{RESET}")

@click.command()
def show_longest_streak():
    """
    Display the longest streak among all habits, including the unit (day, week, month).
    """
    longest_streak, periodicity = get_longest_streak(tracker.get_habits())
    unit = {"daily": "day", "weekly": "week", "monthly": "month"}.get(periodicity, "period")

    if longest_streak == 0:
        click.echo(f"{CYAN}\nThe longest streak among all habits is: 0 {unit}(s).{RESET}")
        return

    click.echo(f"{CYAN}\nThe longest streak among all habits is: {longest_streak} {unit}(s).{RESET}")

@click.command()
@click.argument('habit_name')
def show_longest_streak_for_habit(habit_name):
    """
    Display the longest streak for a specified habit.

    Args:
        habit_name (str): The name of the habit to display the longest streak for.
    """
    habit = next((h for h in tracker.get_habits() if h.name == habit_name.lower()), None)
    if habit:
        streak, periodicity = get_longest_streak_for_habit(habit)
        unit = {"daily": "day", "weekly": "week", "monthly": "month"}.get(periodicity, "period")
        click.echo(f"{CYAN}\nThe longest streak for the habit '{habit_name.lower()}' is: {streak} {unit}(s).{RESET}")
    else:
        click.echo(f"{CYAN}The habit '{habit_name.lower()}' was not found.{RESET}")

def interactive_menu():
    """
    Display an interactive menu for managing habits, providing a choice of commands to execute.
    """
    while True:
        click.echo(f"{YELLOW}____________________________________________________{RESET}")
        click.echo(f"\nHabit Tracker - Available Commands:")
        click.echo("1. Create a habit")
        click.echo("2. Mark a habit as completed")
        click.echo("3. Edit a habit")
        click.echo("4. Delete a habit")
        click.echo("5. List all habits")
        click.echo("6. List habits by periodicity")
        click.echo("7. Show the longest streak across all habits")
        click.echo("8. Show the longest streak for a specific habit")
        click.echo(f"0. Exit")
        click.echo(f"{YELLOW}____________________________________________________{RESET}")

        choice = click.prompt("Enter the number of the command you want to execute", type=int)

        if choice == 1:
            name = click.prompt(f"{GREEN}Enter habit name{RESET}")
            description = click.prompt(f"{GREEN}Enter habit description{RESET}")
            periodicity = click.prompt(f"{GREEN}Enter periodicity (daily/weekly/monthly){RESET}")
            create_habit.callback(name, description, periodicity)

        elif choice == 2:
            habit_name = click.prompt(f"{GREEN}Enter the name of the habit to complete{RESET}")
            complete_habit.callback(habit_name)

        elif choice == 3:
            name = click.prompt(f"{GREEN}Enter habit name to edit{RESET}")
            habit = tracker.get_habit(name.lower())
            if not habit:
                click.echo(f"{CYAN}Habit '{name}' does not exist. Returning to menu.{RESET}")
                continue

            new_name = input(f"{GREEN}Enter new name (or press Enter to keep current): {RESET}")
            new_description = input(f"{GREEN}Enter new description (or press Enter to keep current): {RESET}")
            new_periodicity = input(f"{GREEN}Enter new periodicity (or press Enter to keep current): {RESET}")

            tracker.edit_habit(
                name,
                new_name if new_name else None,
                new_description if new_description else None,
                new_periodicity if new_periodicity else None
            )
            click.echo(f"{CYAN}The habit '{name}' was updated successfully.{RESET}")

        elif choice == 4:
            habit_name = click.prompt(f"{GREEN}Enter the name of the habit to delete{RESET}")
            delete_habit.callback(habit_name)

        elif choice == 5:
            habits = tracker.habits
            if not habits:
                click.echo(f"\n{CYAN}No habits are currently being tracked.{RESET}")
            else:
                list_all_habits.callback()

        elif choice == 6:
            periodicity = click.prompt(f"{GREEN}Enter periodicity (daily/weekly/monthly){RESET}")
            list_habits_by_periodicity.callback(periodicity)

        elif choice == 7:
            show_longest_streak.callback()

        elif choice == 8:
            habit_name = click.prompt(f"{GREEN}Enter the name of the habit{RESET}")
            show_longest_streak_for_habit.callback(habit_name.lower())

        elif choice == 0:
            click.echo(f"{CYAN}Exiting the Habit Tracker. Goodbye!{RESET}")
            break
        else:
            click.echo(f"{CYAN}Invalid option. Please try again.{RESET}")

cli.add_command(create_habit)
cli.add_command(complete_habit)
cli.add_command(edit_habit)
cli.add_command(delete_habit)
cli.add_command(list_all_habits)
cli.add_command(list_habits_by_periodicity)
cli.add_command(show_longest_streak)
cli.add_command(show_longest_streak_for_habit)

if __name__ == "__main__":
    cli()
