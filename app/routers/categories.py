from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/test")
async def root():
    return {"message": "API test ended successfully"}


@router.post("/", response_model=schemas.CategoryResponse, status_code=201)
def create_category(category : schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = crud.create_category(db=db, category=category)
    if db_category is None:
        raise HTTPException(
            status_code=409,
            detail="Category already exists"
        )
    return db_category


@router.get("/", response_model=list[schemas.CategoryResponse])
def read_categories(skip: int = 0,
                    limit: int = 10,
                    name: str | None = None,
                    db: Session = Depends(get_db)):
    categories = crud.get_categories(db,
                    skip=skip,
                    limit=limit,
                    name=name)
    return categories


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def read_category(category_id: int,
                  db: Session = Depends(get_db)):
    category = crud.get_category(db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=404,
                            detail="Category not found")
    return category


@router.put("/{category_id}", response_model=schemas.CategoryResponse)
def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    updated_category = crud.update_category(db, category_id, category)

    if updated_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return updated_category



@router.delete("/{category_id}", response_model=schemas.CategoryResponse)
def delete_category(category_id: int,
                    db: Session = Depends(get_db)):
    expenses = crud.get_expenses_by_category_id(db, category_id=category_id)
    if expenses:
        raise HTTPException(status_code=409, detail="Cannot delete category")
    else:
        category = crud.delete_category(db=db, category_id=category_id)
        return category