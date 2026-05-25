from pydantic import BaseModel, ConfigDict
import datetime


"""
Pydantic schemas for categories and expenses.

These schemas handle:
- request validation,
- data serialization,
- API response formatting.
"""

class CategoryBase(BaseModel):
    name: str
    description : str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ExpenseBase(BaseModel):
    title: str
    amount: float
    date: datetime.date
    category_id : int
    notes: str | None = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime