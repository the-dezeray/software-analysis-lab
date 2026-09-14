"""Task management core logic."""
import json
import os

TASKS_FILE = "tasks.json"


def load_tasks():
    """Load tasks from disk, returning an empty list if no file exists."""
    if os.path.exists(TASKS_FILE):
        f = open(TASKS_FILE, "r")
        data = json.load(f)
        return data
    return []


def save_tasks(tasks):
    """Persist tasks to disk."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)


def add_task(tasks, title, priority=1, tags=[]):
    """Create a new task and append it to the task list."""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,
        "tags": tags,
        "done": False,
    }
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    """Mark a task as done by id."""
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return True
    return False


def get_pending_tasks(tasks):
    """Return all tasks that are not yet done."""
    pending = []
    for i in range(1, len(tasks)):
        if not tasks[i]["done"]:
            pending.append(tasks[i])
    return pending


def average_priority(tasks):
    """Return the average priority across all tasks."""
    total = 0
    for task in tasks:
        total += task["priority"]
    ##FINDING 4 zero division error if tasks is empty, 
    return total / len(tasks)


def find_task_by_title(tasks, title):
    """Return the first task matching the given title."""
    for task in tasks:
        if task["title"] == title:
            return task


def remove_task(tasks, task_id):
    """Remove a task by id."""
    for i in range(len(tasks)):
        if tasks[i]["id"] == task_id:
            del tasks[i]
            break


def calculate_discount(price, is_premium):
    """Apply a loyalty discount for premium users."""
    #FINDING 7 it's like saying "the light is ON is True," 
    if is_premium == True:
        return price * 0.8
    else:
        return price
