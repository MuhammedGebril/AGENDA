# import the modules and the Task class
import pytest
import sqlite3
from datetime import datetime
from task_model import Task 

# create a fixture to set up and tear down the database connection and cursor
@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        NAME TEXT NOT NULL,
        description TEXT ,
        Due_Date TEXT ,
        priority TEXT ,
        status TEXT ,
        Is_My_Day BOOLEAN ,
        List_Name TEXT
        )""")
    conn.commit()
    yield conn, cur
    conn.close()

# create a fixture to create a sample task object
@pytest.fixture
def task():
    return Task(name="Test Task", description="This is a test task", due_date="2023-12-31", priority="High", status="Completed", is_my_day=1, list_name="Test List")

# test the __init__ method of the Task class
def test_init(task):
    assert task.name == "Test Task"
    assert task.description == "This is a test task"
    assert task.due_date == "2023-12-31"
    assert task.priority == "High"
    assert task.status == "Completed"
    assert task.is_my_day == 1
    assert task.list_name == "Test List"

# test the add_task method of the Task class
def test_add_task(db, task):
    conn, cur = db
    task.add_task()
    cur.execute("SELECT * FROM tasks WHERE name = ?", (task.name,))
    result = cur.fetchone()
    assert result is not None
    assert result[1] == task.name
    assert result[2] == task.description
    assert result[3] == task.due_date
    assert result[4] == task.priority
    assert result[5] == task.status
    assert result[6] == task.is_my_day
    assert result[7] == task.list_name

# test the delete_task method of the Task class
def test_delete_task(db, task):
    conn, cur = db
    task.add_task()
    cur.execute("SELECT id FROM tasks WHERE name = ?", (task.name,))
    task_id = cur.fetchone()[0]
    Task.delete_task(task_id)
    cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    result = cur.fetchone()
    assert result is None

# test the query method of the Task class
def test_query(db, task):
    conn, cur = db
    task.add_task()
    tasks = Task.query(filter="name = 'Test Task'", order="id DESC")
    assert len(tasks) == 1
    assert tasks[0].name == task.name
    assert tasks[0].description == task.description
    assert tasks[0].due_date == task.due_date
    assert tasks[0].priority == task.priority
    assert tasks[0].status == task.status
    assert tasks[0].is_my_day == task.is_my_day
    assert tasks[0].list_name == task.list_name

# test the update method of the Task class
def test_update(db, task):
    conn, cur = db
    task.add_task()
    cur.execute("SELECT id FROM tasks WHERE name = ?", (task.name,))
    task_id = cur.fetchone()[0]
    task.name = "Updated Task"
    task.description = "This is an updated task"
    task.due_date = "2024-01-01"
    task.priority = "Medium"
    task.status = "In progress"
    task.is_my_day = 0
    task.list_name = "Updated List"
    task.update(task_id)
    cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    result = cur.fetchone()
    assert result is not None
    assert result[1] == task.name
    assert result[2] == task.description
    assert result[3] == task.due_date
    assert result[4] == task.priority
    assert result[5] == task.status
    assert result[6] == task.is_my_day
    assert result[7] == task.list_name
