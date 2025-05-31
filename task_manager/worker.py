from datetime import datetime
from sqlalchemy.orm import Session
from .models import Task, Status
from .crud import get_tasks
from .database import get_db

def send_reminder_email(email: str, task_title: str):
    # Placeholder for sending email logic
    print(f"Sending reminder email to {email} for task: {task_title}")

def check_due_tasks():
    db = next(get_db())
    now = datetime.utcnow()
    overdue_tasks = db.query(Task).filter(
        Task.due_date <= now,
        Task.status != Status.COMPLETED,
        Task.reminder_sent == False
    ).all()
    for task in overdue_tasks:
        # Assuming task.user has an email attribute; if not, adjust accordingly
        if hasattr(task.user, "email"):
            send_reminder_email(task.user.email, task.title)
            task.reminder_sent = True
            db.commit()
