#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


DATA_FILE = Path.home() / ".data.json"
# Ensure the parent directory exists (optional here since it's the home directory)
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

# Create the file if it doesn't exist, and initialize with empty JSON
if not DATA_FILE.exists():
    DATA_FILE.write_text(json.dumps({}, indent=2))

def load_tasks():
    """ Have to include a docstring for this basic fucking function because we have to follow best practices that
    some anal autistic retard suggested due to their tics or smth
    BTW this function just checks the json file for the content to be displayed """
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except json.JSONDecodeError:
        print("You're screwed, you should've maintained a copy for you to-do list instead of trusting mathematician"
              "pretending to be engineers")
    return []

def save_tasks(tasks):
    """ Yes you dumb bitch, it writes data to the json, need this because we are using a temp file, them dumping to the json, w rizz"""
    try:

        # Ensure the parent directory exists and overwrites the DATA_FILE(not a bad thing you dumb bitch)
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

        temp_file = DATA_FILE.with_suffix(".tmp")

        with open(temp_file, 'w') as f:
            json.dump(tasks, f , indent = 2)
        os.replace(temp_file, DATA_FILE)
    except IOError as e:
        print(f"⚠️  Failed to save tasks: {str(e)}")
        # Fallback: try direct write if temp file approach fails
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(tasks, f, indent=2)
        except IOError as e2:
            print(f"⚠️  Critical: Could not save tasks at all: {str(e2)}")


def add_tasks(tasks, description):
    """ Adds a new task"""
    new_id = max(task['id'] for task in tasks)+1 if tasks else 1
    tasks.append({
        'id' : new_id,
        'description' : description,
        'created_at' : datetime.now().isoformat(),
        'completed' : False
    })
    save_tasks(tasks)
    print(f"Added task {new_id}: {description}")
    return tasks

def list_tasks(tasks, show_all=False):
    if not tasks:
        print ('No tasks found. Add one with "add" command!')
        return tasks
    filtered = tasks if show_all else [t for t in tasks if not t['completed']]

    if not filtered:
        print("All tasks completed! Add new if you got some new shiz to work on")
        return tasks
    print("\nID Status Description")
    print("-" * 40)
    for task in filtered:
        status = "✓" if task['completed'] else " "
        print(f"{task['id']:3} [{status}]  {task['description']}")
    print(f"\nTotal: {len(filtered)}/{len(tasks)} tasks shown")
    return tasks
def complete_task(tasks, task_id):
    """Mark a task as completed"""
    for task in tasks:
        if task['id'] == task_id:
            if task['completed']:
                print(f"ℹ️  Task #{task_id} is already completed")
            else:
                task['completed'] = True
                save_tasks(tasks)
                print(f"🎯 Completed task #{task_id}: {task['description']}")
            return tasks
    print(f"❌ Task #{task_id} not found")
    return tasks

def remove_task(tasks, task_id):
    """Delete a task by ID"""
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            deleted_description = task['description']
            del tasks[i]
            save_tasks(tasks)
            print(f"🗑️  Removed task #{task_id}: {deleted_description}")
            return tasks
    print(f"❌ Task #{task_id} not found")
    return tasks

def interactive_shell():
    """Run this shit without exiting every damn time"""
    tasks = load_tasks()
    print("\n🌟 Todo List - Interactive Mode (type 'exit' when you're done or 'help' if you're lost)")

    while True:
        try:
            # Read input with basic line editing
            user_input = input("\ntodo> ").strip()

            if not user_input:
                continue

            # Split command and arguments
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if command in ["exit", "quit"]:
                print("\nLater, skater! 👋")
                break

            elif command == "help":
                print("\nCommands you can use:")
                print("  add <description>   - Add a new task")
                print("  list [--all]        - Show tasks (add --all to see completed shit)")
                print("  done <id>           - Mark task as completed")
                print("  remove <id>         - Delete a task (careful, no undo!)")
                print("  help                - Show this useless help")
                print("  exit                - Get me outta here!")

            elif command == "add":
                if not arg:
                    print("Error: WTF you trying to add? Nothing?")
                else:
                    tasks = add_tasks(tasks, arg)

            elif command == "list":
                show_all = "--all" in arg.split()
                tasks = list_tasks(tasks, show_all)

            elif command in ["done", "complete"]:
                try:
                    task_id = int(arg)
                    tasks = complete_task(tasks, task_id)
                except ValueError:
                    print("Error: That ain't no task ID I've ever seen!")

            elif command in ["remove", "delete", "rm"]:
                try:
                    task_id = int(arg)
                    tasks = remove_task(tasks, task_id)
                except ValueError:
                    print("Error: You trying to delete something that doesn't exist?")

            else:
                print(f"WTF is '{command}'? Type 'help' if you're confused")

        except KeyboardInterrupt:
            print("\nNot exiting! Type 'exit' like a normal person")
        except EOFError:
            print("\nSeriously? Ctrl-D? Just type 'exit'")
            sys.stdin = open('/dev/tty') if os.name != 'nt' else open('con:', 'r')


def main():
    # Set up command parser
    parser = argparse.ArgumentParser(
        prog='todo',
        description='Simple CLI Todo List',
        add_help=False
    )
    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Show this help message and exit'
    )

    subparsers = parser.add_subparsers(
        dest='command',
        title='commands',
        description='valid commands',
        metavar='COMMAND'
    )

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('description', help='Task description')

    # List command
    list_parser = subparsers.add_parser('list', help='Show tasks')
    list_parser.add_argument('-a', '--all', action='store_true', help='Show all tasks (including completed)')

    # Complete command
    done_parser = subparsers.add_parser('done', help='Mark task as completed')
    done_parser.add_argument('id', type=int, help='Task ID to complete')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Delete a task')
    remove_parser.add_argument('id', type=int, help='Task ID to remove')

    # Interactive command
    subparsers.add_parser('interactive', help='Launch persistent mode')

    # Help command
    subparsers.add_parser('help', help='Show help message')

    # Handle no command provided by launching interactive mode
    if len(sys.argv) == 1:
        interactive_shell()
        return

    # Parse arguments
    args = parser.parse_args()

    # Handle help command
    if args.command == 'help':
        parser.print_help()
        return

    # Handle interactive command
    if args.command == 'interactive':
        interactive_shell()
        return

    tasks = load_tasks()

    # Execute commands
    if args.command == 'add':
        tasks = add_tasks(tasks, args.description)
    elif args.command == 'list':
        tasks = list_tasks(tasks, args.all)
    elif args.command == 'done':
        tasks = complete_task(tasks, args.id)
    elif args.command == 'remove':
        tasks = remove_task(tasks, args.id)


if __name__ == '__main__':
    main()