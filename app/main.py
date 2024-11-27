from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, models, schemas, dependencies
from app.database import engine, SessionLocal
from app.security import create_access_token, verify_password

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(SessionLocal)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user is None or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=HTTPException(status.HTTP_401_UNAUTHORIZED), detail="Invalid credentials")
    token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/user", response_model=schemas.UserInDB)
def create_user(user: schemas.UserCreate, db: Session = Depends(SessionLocal)):
    return crud.create_user(db=db, user=user)


@app.get("/user/{user_id}", response_model=schemas.UserInDB)
def get_user(user_id: int, db: Session = Depends(SessionLocal)):
    return crud.get_user(db=db, user_id=user_id)


@app.patch("/user/{user_id}", response_model=schemas.UserInDB)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(SessionLocal)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


@app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(SessionLocal)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db=db, user_id=user_id)
