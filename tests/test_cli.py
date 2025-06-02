import pytest
from typer.testing import CliRunner
from task_manager.cli import app
from task_manager.database import init_db, get_db
from task_manager.models import User
import hashlib

runner = CliRunner()

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()
    yield

def test_task_commands():
    # Add a user for user_id reference
    db = next(get_db())
    password_hash = hashlib.sha256("password".encode()).hexdigest()
    user = User(username="testuser", password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Add a task
    result = runner.invoke(app, ["task", "add", "Test Task", "--description", "desc", "--due-date", "2099-12-31", "--priority", "medium", "--user-id", str(user.id)])
    assert result.exit_code == 0
    assert "Task created with ID" in result.output

    # List tasks
    result = runner.invoke(app, ["task", "list"])
    assert result.exit_code == 0
    assert "Test Task" in result.output

    # Show task details (assuming ID 1)
    result = runner.invoke(app, ["task", "show", "1"])
    assert result.exit_code == 0
    assert "Test Task" in result.output

    # Update task
    result = runner.invoke(app, ["task", "update", "1", "--title", "Updated Task", "--status", "completed"])
    assert result.exit_code == 0
    assert "updated successfully" in result.output

    # Delete task
    result = runner.invoke(app, ["task", "delete", "1"])
    assert result.exit_code == 0
    assert "deleted successfully" in result.output

def test_category_commands():
    # Add category
    result = runner.invoke(app, ["category", "category-add", "Work"])
    assert result.exit_code == 0
    assert "Category created with ID" in result.output

    # List categories
    result = runner.invoke(app, ["category", "category-list"])
    assert result.exit_code == 0
    assert "Work" in result.output

    # Delete category (assuming ID 1)
    result = runner.invoke(app, ["category", "category-delete", "1"])
    assert result.exit_code == 0
    assert "deleted successfully" in result.output

def test_user_commands():
    # Register user
    result = runner.invoke(app, ["user", "register", "cliuser"], input="password\npassword\n")
    assert result.exit_code == 0
    assert "registered successfully" in result.output

    # Login user
    result = runner.invoke(app, ["user", "login", "cliuser"], input="password\n")
    assert result.exit_code == 0
    assert "Login successful" in result.output
