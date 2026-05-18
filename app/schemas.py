from pydantic import BaseModel, ConfigDict
import datetime

class CategoryBase(BaseModel):
    name: str
    description : str | None = None


class CategoryCreate(CategoryBase):
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


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime