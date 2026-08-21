"""
Simple Command-Line To-Do List App
Run with: python todo.py
Tasks are saved to tasks.json so they persist between runs.
"""

import json
import os

# File where tasks are stored (created automatically in the same folder as this script)
TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from the JSON file. Returns an empty list if the file doesn't exist yet."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Write the current list of tasks to the JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def show_menu():
    print("\n===== TO-DO LIST =====")
    print("1. View tasks")
    print("2. Add task")
    print("3. Mark task as done")
    print("4. Delete task")
    print("5. Quit")


def view_tasks(tasks):
    if not tasks:
        print("\nNo tasks yet. Add one!")
        return
    print("\nYour tasks:")
    for i, task in enumerate(tasks, start=1):
        status = "[x]" if task["done"] else "[ ]"
        print(f"{i}. {status} {task['title']}")


def add_task(tasks):
    title = input("Enter new task: ").strip()
    if title == "":
        print("Task can't be empty.")
        return
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")


def mark_done(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to mark done: "))
        tasks[num - 1]["done"] = True
        save_tasks(tasks)
        print("Marked as done.")
    except (ValueError, IndexError):
        print("Invalid task number.")


def delete_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        num = int(input("Enter task number to delete: "))
        removed = tasks.pop(num - 1)
        save_tasks(tasks)
        print(f"Deleted: {removed['title']}")
    except (ValueError, IndexError):
        print("Invalid task number.")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
