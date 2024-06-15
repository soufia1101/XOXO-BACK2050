from pydantic import BaseModel


class User(BaseModel):
    Name: str
    Score: int

class Game(BaseModel):

    Name: str
    State: str
