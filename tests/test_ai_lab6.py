"""Lab 6 - AI-GENERATED tests (Muse Spark, free tier). Unedited output."""
from app.tasks import add_task, find_task_by_title, remove_task
from app.storage import format_task_report


def _two_tasks():
    tasks = []
    add_task(tasks, "Task A")
    add_task(tasks, "Task B")
    return tasks


def test_ai_find_returns_matching_task():
    tasks = _two_tasks()
    result = find_task_by_title(tasks, "Task A")
    assert result is not None
    assert result["title"] == "Task A"


def test_ai_find_returns_none_when_missing():
    tasks = _two_tasks()
    assert find_task_by_title(tasks, "Nope") is None


def test_ai_find_empty_list_returns_none():
    assert find_task_by_title([], "Task A") is None


def test_ai_remove_deletes_task():
    tasks = _two_tasks()
    remove_task(tasks, 1)
    assert len(tasks) == 1


def test_ai_remove_nonexistent_does_not_crash():
    tasks = _two_tasks()
    remove_task(tasks, 99)
    assert len(tasks) == 2


def test_ai_report_returns_string():
    tasks = _two_tasks()
    report = format_task_report(tasks)
    assert isinstance(report, str)


def test_ai_report_contains_task_title():
    tasks = _two_tasks()
    report = format_task_report(tasks)
    assert "Task A" in report


def test_ai_report_empty_list():
    assert format_task_report([]) == ""
