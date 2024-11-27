from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password, verify_password
from app.security import create_access_token


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_advertisement(db: Session, advertisement_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()


def create_advertisement(db: Session, advertisement: schemas.AdvertisementCreate, user_id: int):
    db_advertisement = models.Advertisement(**advertisement.dict(), author_id=user_id)
    db.add(db_advertisement)
    db.commit()
    db.refresh(db_advertisement)
    return db_advertisement


def update_advertisement(db: Session, advertisement_id: int, advertisement: schemas.AdvertisementUpdate, user_id: int):
    db_advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if db_advertisement and db_advertisement.author_id == user_id:
        for key, value in advertisement.dict(exclude_unset=True).items():
            setattr(db_advertisement, key, value)
        db.commit()
        db.refresh(db_advertisement)
        return db_advertisement
    return None


def delete_advertisement(db: Session, advertisement_id: int, user_id: int):
    db_advertisement = db.query(models.Advertisement).filter(models.Advertisement.id == advertisement_id).first()
    if db_advertisement and db_advertisement.author_id == user_id:
        db.delete(db_advertisement)
        db.commit()
        return db_advertisement
    return None
