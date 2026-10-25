"""Lab 7 - targeted tests for surviving AI-suite mutants."""
from app.storage import format_task_report
from app.tasks import add_task


def _task(title):
    tasks = []
    add_task(tasks, title)
    return tasks


def test_kill_47_exact_task_prefix():
    assert format_task_report(_task("Task A")).startswith("Task #1:")


def test_kill_51_exact_colon_separator():
    assert format_task_report(_task("Task A")) == "Task #1: Task A"


def test_kill_55_single_newline_between_tasks():
    tasks = []
    add_task(tasks, "Task A")
    add_task(tasks, "Task B")
    assert format_task_report(tasks) == "Task #1: Task A\nTask #2: Task B"
