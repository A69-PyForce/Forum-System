from pydantic import BaseModel

class User(BaseModel):
    """
    Model User, corresponding to the Database.
    """
    id: int | None = None
    username: str
    password: str
    is_admin: bool

class Topic(BaseModel):
    pass

class Vote(BaseModel):
    pass

class Reply(BaseModel):
    pass

class Message(BaseModel):
    pass

class Category(BaseModel):
    pass