from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.schemas import ExpenseCreate


router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=schemas.ExpenseResponse, summary="Create a new expense")
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    category = crud.get_category(db, expense.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    else:
        db_expense = crud.create_expense(db=db, expense=expense)
        return db_expense


@router.get("/", response_model=list[schemas.ExpenseResponse], summary="Get all expenses")
def read_expenses(skip: int = 0, limit: int = 10, category_id: int | None = None,
                  db: Session = Depends(get_db)):
    expenses = crud.get_expenses(db,
                                skip=skip,
                                limit=limit,
                                category_id=category_id)
    return expenses


@router.get("/{expense_id}", response_model=schemas.ExpenseResponse, summary="Get expense by ID")
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.get_expense(db, expense_id=expense_id)
    if expense is None:
        raise HTTPException(status_code=404,
                            detail="Expense not found")
    return expense


@router.put("/{expense_id}", response_model=schemas.ExpenseResponse, summary="Update an expense")
def update_expense(expense_id: int, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    updated_expense = crud.update_expense(db, expense_id, expense)

    if updated_expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return updated_expense


@router.delete("/{expense_id}", response_model=schemas.ExpenseResponse, summary="Delete an expense")
def delete_response(expense_id: int, db: Session = Depends(get_db)):
    expense = crud.delete_expense(db=db, expense_id=expense_id)
    if expense is None:
        raise HTTPException(status_code=404,
                            detail="Expense not found")
    return expense