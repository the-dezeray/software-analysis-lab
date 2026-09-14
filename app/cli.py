"""Command-line entry point for the Task Manager sample app."""
from app.tasks import load_tasks, save_tasks, add_task, get_pending_tasks
from app.storage import format_task_report


def main():
    tasks = load_tasks()
    print("Loaded", len(tasks), "tasks")
    print(format_task_report(tasks))
    pending = get_pending_tasks(tasks)
    print("Pending tasks:", len(pending))


if __name__ == "__main__":
    main()
