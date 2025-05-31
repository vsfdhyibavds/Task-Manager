import pytest
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from task_manager.models import Base, User, Task, Category, Priority, Status
from task_manager.crud import (
    create_user, get_user_by_username, create_task, get_task, update_task, delete_task,
    create_category, get_category, update_category, delete_category,
    update_user, delete_user
)
from task_manager.worker import check_due_tasks

# Setup in-memory SQLite for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import subprocess

@pytest.fixture(scope="module")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_user_crud(db):
    user = create_user(db, "testuser", "hashedpassword")
    assert user.username == "testuser"
    fetched = get_user_by_username(db, "testuser")
    assert fetched.id == user.id
    updated = update_user(db, user.id, username="newname")
    assert updated.username == "newname"
    deleted = delete_user(db, user.id)
    assert deleted.id == user.id
    assert get_user_by_username(db, "newname") is None

def test_category_crud(db):
    category = create_category(db, "Work")
    assert category.name == "Work"
    fetched = get_category(db, category.id)
    assert fetched.id == category.id
    updated = update_category(db, category.id, "Personal")
    assert updated.name == "Personal"
    deleted = delete_category(db, category.id)
    assert deleted.id == category.id
    assert get_category(db, category.id) is None

def test_task_crud(db):
    category = create_category(db, "TestCat")
    user = create_user(db, "taskuser", "passhash")
    due_date = datetime.utcnow() + timedelta(days=1)
    task = create_task(db, "Test Task", "Desc", due_date, Priority.MEDIUM, category.id, Status.PENDING, user.id)
    assert task.title == "Test Task"
    fetched = get_task(db, task.id)
    assert fetched.id == task.id
    updated = update_task(db, task.id, title="Updated Task")
    assert updated.title == "Updated Task"
    deleted = delete_task(db, task.id)
    assert deleted.id == task.id
    assert get_task(db, task.id) is None

def test_check_due_tasks(db, capsys):
    user = create_user(db, "reminderuser", "passhash")
    due_date = datetime.utcnow() - timedelta(days=1)
    task = create_task(db, "Due Task", "Desc", due_date, Priority.HIGH, None, Status.PENDING, user.id)
    # Add email attribute to user for test
    user.email = "user@example.com"
    db.commit()
    check_due_tasks()
    captured = capsys.readouterr()
    assert "Sending reminder email" in captured.out
    # Verify reminder_sent is set
    updated_task = get_task(db, task.id)
    assert updated_task.reminder_sent is True
