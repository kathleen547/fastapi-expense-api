from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas


def get_categories(db: Session, skip: int = 0, limit: int = 10,
                   name: str = None):
    """
    Returns a list of categories with optional pagination and filtering.
    """
    query = db.query(models.Category)
    if name:
        query = query.filter(name == models.Category.name)
    return query.offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    """
    Returns a category by its ID.
    """
    return db.query(models.Category).filter(category_id == models.Category.id).first()


def get_category_by_name(db: Session, name: str):
    """
    Returns a category by its name.
    """
    return db.query(models.Category).filter(name == models.Category.name).first()


def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Creates a new category in the database.
    Returns the created category object.
    """
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


def update_category(db: Session, category_id : int, category: schemas.CategoryUpdate):
    """
    Updates an existing category.
    Returns the updated category object.
    """
    db_category = db.query(models.Category).filter(category_id == models.Category.id).first()
    if db_category is None:
        return None

    db_category.name = category.name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(db: Session, category_id: int):
    """
    Deletes a category from the database.
    """
    category = get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    db.delete(category)
    db.commit()
    return category


def create_expense(db: Session, expense: schemas.ExpenseCreate):
    """
    Creates a new expense in the database.
    Returns the created expense object.
    """
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
    """
    Returns a list of expenses with optional pagination and filtering.
    """
    query = db.query(models.Expense)
    if category_id:
        query = query.filter(category_id == models.Expense.category_id)
    return query.offset(skip).limit(limit).all()


def get_expense(db: Session, expense_id: int):
    """
    Returns an expense by its ID
    """
    return db.query(models.Expense).filter(expense_id == models.Expense.id).first()


def get_expenses_by_category_id(db: Session, category_id: int):
    """
    Returns an expense by its category_id
    """
    return db.query(models.Expense).filter(category_id == models.Expense.category_id).all()


def update_expense(db: Session, expense_id : int, expense: schemas.ExpenseUpdate):
    """
    Updates an existing expense.
    Returns the updated expense object.
    """
    db_expense = db.query(models.Expense).filter(expense_id == models.Expense.id).first()
    if db_expense is None:
        return None

    db_expense.title = expense.title
    db_expense.amount = expense.amount
    db_expense.date = expense.date
    db_expense.category_id = expense.category_id
    db_expense.notes = expense.notes

    db.commit()
    db.refresh(db_expense)

    return db_expense

def delete_expense(db: Session, expense_id: int):
    """
    Deletes an expense from the database.
    """
    expense = get_expense(db, expense_id=expense_id)
    if expense is None:
        return None

    db.delete(expense)
    db.commit()
    return expense
