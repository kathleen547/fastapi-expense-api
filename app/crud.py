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
