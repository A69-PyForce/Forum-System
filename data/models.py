from pydantic import BaseModel

class User(BaseModel):
    """
    Model User, corresponding to the Database.
    """
    id: int | None = None
    username: str
    password: str
    is_admin: int # we are using tinyint which is 0 and 1 for true or false

class Topic(BaseModel):
    id: int | None
    title: str
    content: str
    categories_id: int
    user_id: int
    is_locked: int

class Vote(BaseModel):
    id: int
    reply_id: int
    users_id: int

class Reply(BaseModel):
    id: int
    text: str
    topics_id: int
    user_id: int

class Message(BaseModel):
    id: int
    text: str
    sender_id: int
    receiver_id: int

class Category(BaseModel):
    id: int
    name: str
    is_private: int  # 0 or 1
    is_locked: int  # same 0 or 1

class CategoryUserAccess(BaseModel):
    categories_id: int
    users_id: int
    has_right_access: int # 0 or 1