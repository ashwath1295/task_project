import argparse
import json
from pathlib import Path

TASKS_FILE = "tasks.json"

# Load tasks from the file
def load_tasks():
    if not Path(TASKS_FILE).exists():
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

# Save tasks to the file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

# Add a task
def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description, "done": False})
    save_tasks(tasks)
    print(f"Added task: {description}")

# View all tasks
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        status = "✔" if task["done"] else "✘"
        print(f"{i}. [{status}] {task['description']}")

# Mark a task as done
def mark_done(index):
    tasks = load_tasks()
    try:
        tasks[index - 1]["done"] = True
        save_tasks(tasks)
        print(f"Marked task {index} as done.")
    except IndexError:
        print(f"No task found with index {index}.")

# Delete a task
def delete_task(index):
    tasks = load_tasks()
    try:
        removed = tasks.pop(index - 1)
        save_tasks(tasks)
        print(f"Deleted task: {removed['description']}")
    except IndexError:
        print(f"No task found with index {index}.")

# Main function
def main():
    parser = argparse.ArgumentParser(description="To-Do List CLI Application")
    subparsers = parser.add_subparsers(dest="command")

    # Add task command
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("description", type=str, help="Description of the task")

    # View tasks command
    subparsers.add_parser("view", help="View all tasks")

    # Mark done command
    parser_done = subparsers.add_parser("done", help="Mark a task as done")
    parser_done.add_argument("index", type=int, help="Index of the task to mark as done")

    # Delete task command
    parser_delete = subparsers.add_parser("delete", help="Delete a task")
    parser_delete.add_argument("index", type=int, help="Index of the task to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "view":
        view_tasks()
    elif args.command == "done":
        mark_done(args.index)
    elif args.command == "delete":
        delete_task(args.index)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
