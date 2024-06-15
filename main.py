from fastapi import FastAPI, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import basemodels
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

models.Base.metadata.create_all(engine)



@app.get("/players", response_model=list[basemodels.User])
def getPlayers(db : db_dependency):
    return db.query(models.Users).all()


@app.post("/Players", response_model=basemodels.User)
def CreatePlayer(user: basemodels.User ,db: db_dependency):
    db_user = db.query(models.Users).filter(models.Users.Name == user.Name).first()
    if db_user:
        return db_user
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/Play', response_model=list[basemodels.User])
def ChangeScore(users: list[basemodels.Game], db : db_dependency):
    print(users)
    db_user1 = db.query(models.Users).filter(models.Users.Name == users[0].Name).first()
    db_user2 = db.query(models.Users).filter(models.Users.Name == users[1].Name).first()
    print(db_user1)
    print(db_user2)
    if users[0].State == "WIN":
        db_user1.Score += 1
    else:
        db_user1.Score -= 1
    if users[1].State == "WIN":
        db_user2.Score += 1
    else:
        db_user2.Score -= 1
    db.commit()
    return {db_user1,db_user2}
