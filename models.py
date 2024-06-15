from database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "Users"

    Id = Column(Integer, primary_key=True, index=True)
    Name = Column(String)
    Score = Column(Integer)