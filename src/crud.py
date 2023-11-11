from sqlalchemy.orm import Session

from . import models


def get_users(db: Session):
    return db.query(models.User).limit(1).all()


def get_user_details(db: Session):
    return db.query(models.UserDetails).limit(1).all()
