import typer
from rich.console import Console
from rich.table import Table

from task_manager.database import get_db
from task_manager.crud import create_category, get_categories, delete_category
