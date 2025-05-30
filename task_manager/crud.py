from sqlalchemy.orm import Session
from datetime import datetime
from .models import Task, Category, Priority

# Task CRUD operations
def create_task(db: Session, title: str, description: str, due_date: datetime,
               priority: Priority, category_id: int = None):
    task = Task(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        category_id=category_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Task).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, **kwargs):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        for key, value in kwargs.items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task

# Category CRUD operations
def create_category(db: Session, name: str):
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def update_category(db: Session, category_id: int, name: str):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.name = name
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category