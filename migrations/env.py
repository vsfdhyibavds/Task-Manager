import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from task_manager.models import Base
from task_manager.config import SQLALCHEMY_DATABASE_URI

# ...

target_metadata = Base.metadata