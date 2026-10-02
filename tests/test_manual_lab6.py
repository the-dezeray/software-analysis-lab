"""Lab 6 - MANUAL tests (written without AI assistance) for the same 3 functions."""
from app.tasks import add_task, find_task_by_title, remove_task
from app.storage import format_task_report


def test_manual_find_returns_exact_task_dict():
    tasks = []
    created = add_task(tasks, "Write report", priority=2)
    found = find_task_by_title(tasks, "Write report")
    assert found == created
    assert found == {"id": 1, "title": "Write report", "priority": 2,
                     "tags": [], "done": False}


def test_manual_find_returns_first_match_on_duplicates():
    tasks = []
    first = add_task(tasks, "Same")
    add_task(tasks, "Same")
    assert find_task_by_title(tasks, "Same") == first
    assert find_task_by_title(tasks, "Same")["id"] == 1


def test_manual_find_is_case_sensitive():
    tasks = []
    add_task(tasks, "Task A")
    assert find_task_by_title(tasks, "task a") is None
    assert find_task_by_title(tasks, "TASK A") is None


def test_manual_find_missing_and_empty():
    assert find_task_by_title([], "Anything") is None
    tasks = []
    add_task(tasks, "Task A")
    assert find_task_by_title(tasks, "Task B") is None


def test_manual_remove_keeps_the_right_task():
    tasks = []
    add_task(tasks, "Task A")
    task_b = add_task(tasks, "Task B")
    assert remove_task(tasks, 1) is None
    assert tasks == [task_b]
    assert tasks[0]["id"] == 2
    assert tasks[0]["title"] == "Task B"


def test_manual_remove_nonexistent_leaves_list_untouched():
    tasks = []
    add_task(tasks, "Task A")
    snapshot = [dict(t) for t in tasks]
    assert remove_task(tasks, 99) is None
    assert tasks == snapshot


def test_manual_remove_from_empty_list():
    tasks = []
    assert remove_task(tasks, 1) is None
    assert tasks == []


def test_manual_report_single_task_exact_string():
    tasks = []
    add_task(tasks, "Write report")
    assert format_task_report(tasks) == "Task #1: Write report"


def test_manual_report_two_tasks_joined_with_newline():
    tasks = []
    add_task(tasks, "Task A")
    add_task(tasks, "Task B")
    assert format_task_report(tasks) == "Task #1: Task A\nTask #2: Task B"


def test_manual_report_empty_list():
    assert format_task_report([]) == ""
