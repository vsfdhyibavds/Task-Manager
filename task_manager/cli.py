import typer
from typing import Optional
from datetime import datetime
from enum import Enum
from typing import Optional
from rich.console import Console
from rich.table import Table
import typer
import getpass
import hashlib

from .models import Priority
from .database import get_db, init_db
from .crud import (
    create_task, get_task, get_tasks, update_task, delete_task,
    create_category, get_category, get_categories, update_category, delete_category,
    create_user, get_user_by_username
)

app = typer.Typer()
console = Console()

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Status(str, Enum):
    pending = "pending"
    completed = "completed"

@app.command()
def init():
    """Initialize the database"""
    init_db()
    console.print("[green]Database initialized successfully![/green]")

@app.command()
def add(
    title: str,
    description: Optional[str] = typer.Option(None, "--description", "-d"),
    due_date: Optional[str] = typer.Option(None, "--due-date", "-dd"),
    priority: Priority = typer.Option(Priority.medium, "--priority", "-p"),
    category_id: Optional[int] = typer.Option(None, "--category-id", "-c"),
    status: Status = typer.Option(Status.pending, "--status", "-s"),
    user_id: Optional[int] = typer.Option(None, "--user-id", "-u")
):
    """Add a new task"""
    db = next(get_db())

    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None

    task = create_task(
        db=db,
        title=title,
        description=description,
        due_date=due_date_obj,
        priority=priority,
        category_id=category_id,
        status=status,
        user_id=user_id
    )

    console.print(f"[green]Task created with ID: {task.id}[/green]")

@app.command()
def list(
    status: Optional[Status] = typer.Option(None, "--status", "-s", help="Filter tasks by status")
):
    """List all tasks"""
    db = next(get_db())
    tasks = get_tasks(db, status=status.value if status else None)

    table = Table(title="Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Priority")
    table.add_column("Status")
    table.add_column("Category")

    for task in tasks:
        table.add_row(
            str(task.id),
            task.title,
            task.description or "",
            task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            task.priority,
            task.status,
            task.category.name if task.category else ""
        )

    console.print(table)

@app.command()
def show(task_id: int):
    """Show details of a specific task"""
    db = next(get_db())
    task = get_task(db, task_id)

    if not task:
        console.print(f"[red]Task with ID {task_id} not found[/red]")
        raise typer.Exit(1)

    table = Table(title=f"Task {task.id}")
    table.add_column("Field", style="cyan")
    table.add_column("Value")

    table.add_row("Title", task.title)
    table.add_row("Description", task.description or "")
    table.add_row("Due Date", task.due_date.strftime("%Y-%m-%d") if task.due_date else "")
    table.add_row("Priority", task.priority)
    table.add_row("Category", task.category.name if task.category else "")
    table.add_row("Created At", task.created_at.strftime("%Y-%m-%d %H:%M:%S"))

    console.print(table)

@app.command()
def update(
    task_id: int,
    title: Optional[str] = typer.Option(None, "--title", "-t"),
    description: Optional[str] = typer.Option(None, "--description", "-d"),
    due_date: Optional[str] = typer.Option(None, "--due-date", "-dd"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p"),
    category_id: Optional[int] = typer.Option(None, "--category-id", "-c"),
    status: Optional[Status] = typer.Option(None, "--status", "-s")
):
    """Update a task"""
    db = next(get_db())

    update_data = {}
    if title:
        update_data["title"] = title
    if description:
        update_data["description"] = description
    if due_date:
        update_data["due_date"] = datetime.strptime(due_date, "%Y-%m-%d")
    if priority:
        update_data["priority"] = priority
    if category_id:
        update_data["category_id"] = category_id
    if status:
        update_data["status"] = status

    task = update_task(db, task_id, **update_data)

    if task:
        console.print(f"[green]Task {task_id} updated successfully![/green]")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")
        raise typer.Exit(1)

@app.command()
def delete(task_id: int):
    """Delete a task"""
    db = next(get_db())
    task = delete_task(db, task_id)

    if task:
        console.print(f"[green]Task {task_id} deleted successfully![/green]")
    else:
        console.print(f"[red]Task with ID {task_id} not found[/red]")
        raise typer.Exit(1)

# Category commands
@app.command()
def category_add(name: str):
    """Add a new category"""
    db = next(get_db())
    category = create_category(db, name)
    console.print(f"[green]Category created with ID: {category.id}[/green]")

@app.command()
def category_list():
    """List all categories"""
    db = next(get_db())
    categories = get_categories(db)

    table = Table(title="Categories")
    table.add_column("ID", style="cyan")
    table.add_column("Name")

    for category in categories:
        table.add_row(str(category.id), category.name)

    console.print(table)

@app.command()
def category_delete(category_id: int):
    """Delete a category"""
    db = next(get_db())
    category = delete_category(db, category_id)

    if category:
        console.print(f"[green]Category {category_id} deleted successfully![/green]")
    else:
        console.print(f"[red]Category with ID {category_id} not found[/red]")
        raise typer.Exit(1)

@app.command()
def register(username: str):
    """Register a new user"""
    db = next(get_db())
    existing_user = get_user_by_username(db, username)
    if existing_user:
        console.print(f"[red]Username '{username}' is already taken.[/red]")
        raise typer.Exit(1)
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm Password: ")
    if password != password_confirm:
        console.print("[red]Passwords do not match.[/red]")
        raise typer.Exit(1)
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = create_user(db, username, password_hash)
    console.print(f"[green]User '{username}' registered successfully with ID: {user.id}[/green]")

@app.command()
def login(username: str):
    """Login a user and return a dummy token"""
    db = next(get_db())
    user = get_user_by_username(db, username)
    if not user:
        console.print(f"[red]User '{username}' not found.[/red]")
        raise typer.Exit(1)
    password = getpass.getpass("Password: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != user.password_hash:
        console.print("[red]Invalid password.[/red]")
        raise typer.Exit(1)
    # For simplicity, return a dummy token (in real app, generate JWT)
    token = f"token-for-user-{user.id}"
    console.print(f"[green]Login successful. Token: {token}[/green]")

if __name__ == "__main__":
    app()
