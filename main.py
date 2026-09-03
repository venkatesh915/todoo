from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base
from schemas import UserCreate, UserResponse
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database connection
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# HOME
@app.get("/")
def home():
    return {
        "message": "welcome"
    }


# POST - CREATE USER
@app.post("/users", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


# GET - GET ALL USERS
@app.get("/users", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


# PUT - UPDATE USER
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):

    updated_user = crud.update_user(
        db,
        user_id,
        user
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user


# DELETE - DELETE USER
@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_user(db, user_id)