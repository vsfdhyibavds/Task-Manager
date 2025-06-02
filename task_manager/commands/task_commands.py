from datetime import datetime
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table

from task_manager.database import get_db
from task_manager.crud import (
    create_task, get_task, get_tasks, update_task, delete_task
)
from task_manager.models import Priority, Status

app = typer.Typer()
console = Console()

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
