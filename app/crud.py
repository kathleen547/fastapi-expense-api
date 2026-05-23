from sqlalchemy.orm import Session

from app import models, schemas


def get_categories(db: Session, skip: int = 0, limit: int = 10,
                   name: str = None):
    query = db.query(models.Category)
    if name:
        query = query.filter(name == models.Category.name)
    return query.offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(category_id == models.Category.id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(models.Category).filter(name == models.Category.name).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    existing_category = get_category_by_name(db, category.name)

    if existing_category:
        return None

    db_category = models.Category(
        name=category.name,
        description=category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id=category_id)
    if category is None:
        return None

    db.delete(category)
    db.commit()
    return category


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        date=expense.date,
        category_id=expense.category_id,
        notes=expense.notes
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, skip: int = 0, limit: int = 10,
                   category_id: int | None = None):
    query = db.query(models.Expense)
    if category_id:
        query = query.filter(category_id == models.Expense.category_id)
    return query.offset(skip).limit(limit).all()


def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(expense_id == models.Expense.id).first()


def delete_expense(db: Session, expense_id: int):
    expense = get_expense(db, expense_id=expense_id)
    if expense is None:
        return None

    db.delete(expense)
    db.commit()
    return expense
