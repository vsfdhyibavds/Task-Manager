import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# Database configuration
DB_NAME = os.getenv("DB_NAME", "tasks.db")
DB_PATH = BASE_DIR / DB_NAME
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

# Alembic configuration
ALEMBIC_INI_PATH = BASE_DIR.parent / "alembic.ini"