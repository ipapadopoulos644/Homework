"""A simple command-line task manager."""

import json
from pathlib import Path


TASKS_FILE = Path(__file__).with_name("tasks.json")


MENU = """
1. Add a task
2. Show tasks
3. Complete a task
4. Delete a task
5. Exit
"""


def main():
    """Run the interactive application menu."""
    tasks = load_tasks()

    while True:
        print(MENU)
        choice = input("Choose an action: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            show_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


def save_tasks(tasks):
    """Save all tasks to the JSON file."""
    TASKS_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_tasks():
    """Load tasks from disk, creating an empty file when necessary."""
    if not TASKS_FILE.exists():
        save_tasks([])
        return []

    try:
        tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print("Warning: tasks.json could not be read. Starting with an empty list.")
        return []

    if not isinstance(tasks, list):
        print("Warning: tasks.json has an invalid format. Starting with an empty list.")
        return []

    return tasks


def show_tasks(tasks):
    """Print the current task list with completion markers."""
    if not tasks:
        print("No tasks found.")
        return

    for number, task in enumerate(tasks, start=1):
        marker = "x" if task.get("completed", False) else " "
        print(f'{number}. [{marker}] {task.get("title", "Untitled task")}')


def add_task(tasks):
    """Ask for a title and add a new incomplete task."""
    title = input("Enter the task: ").strip()

    if not title:
        print("A task cannot be empty.")
        return

    tasks.append({"title": title, "completed": False})
    save_tasks(tasks)
    print("Task added.")


def _choose_task(tasks, action):
    """Return the selected task index, or None for invalid input."""
    if not tasks:
        print(f"No tasks to {action}.")
        return None

    show_tasks(tasks)
    raw_number = input("Enter the task number: ").strip()

    try:
        number = int(raw_number)
    except ValueError:
        print("Invalid number. Enter a whole number from the list.")
        return None

    if number < 1 or number > len(tasks):
        print("Task number is out of range.")
        return None

    return number - 1


def complete_task(tasks):
    """Mark a selected task as completed."""
    task_index = _choose_task(tasks, "complete")
    if task_index is None:
        return

    if tasks[task_index].get("completed", False):
        print("This task is already completed.")
        return

    tasks[task_index]["completed"] = True
    save_tasks(tasks)
    print("Task completed.")


def delete_task(tasks):
    """Delete a selected task."""
    task_index = _choose_task(tasks, "delete")
    if task_index is None:
        return

    deleted_task = tasks.pop(task_index)
    save_tasks(tasks)
    print(f'Task deleted: {deleted_task.get("title", "Untitled task")}')


if __name__ == "__main__":
    main()
