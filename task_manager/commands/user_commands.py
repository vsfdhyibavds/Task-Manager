import typer
import getpass
import hashlib
from rich.console import Console

from task_manager.database import get_db
from task_manager.crud import create_user, get_user_by_username

app = typer.Typer()
console = Console()

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
