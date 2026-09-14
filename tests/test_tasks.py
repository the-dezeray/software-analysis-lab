from app.tasks import (
    add_task,
    complete_task,
    get_pending_tasks,
    average_priority,
    calculate_discount,
)


def test_add_task_creates_task():
    tasks = []
    task = add_task(tasks, "Write report")
    assert len(tasks) == 1
    assert task["title"] == "Write report"


def test_complete_task_marks_done():
    tasks = []
    add_task(tasks, "Write report")
    assert complete_task(tasks, 1) is True
    assert tasks[0]["done"] is True


def test_get_pending_tasks_includes_first_task():
    tasks = []
    add_task(tasks, "Task A")
    add_task(tasks, "Task B")
    pending = get_pending_tasks(tasks)
    assert len(pending) == 2  # fails: off-by-one skips index 0


def test_average_priority_of_empty_list():
    tasks = []
    assert average_priority(tasks) == 0  # fails: ZeroDivisionError


def test_calculate_discount_for_premium_user():
    assert calculate_discount(100, True) == 80


def test_calculate_discount_for_regular_user():
    assert calculate_discount(100, False) == 100
