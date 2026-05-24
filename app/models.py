from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates

from app.database import Base

class Category(Base):
    __tablename__= "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    expenses = relationship("Expense", back_populates = "category")


class Expense(Base):
    __tablename__= "expense"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates = "expenses")
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    @validates("amount")
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError(f"Amount must be greater than 0")
        return amount
