from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Annotated

class User(BaseModel):
    id: int | None = None
    username: Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9]+$')] # Only letters, numbers and no special characters for usernames.
    password: str
    is_admin: int # we are using tinyint which is 0 and 1 for true or false
    
    @classmethod
    def from_query_result(cls, id, username, password, is_admin):
        return cls(
            id=id,
            username=username,
            password=password,
            is_admin=is_admin
        )

class UserLoginData(BaseModel):
    username: str
    password: str

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
    id: int | None = None # set by db
    text: str
    conversation_id: int | None = None # set inside conv router
    sender_id: int | None = None # set by the u_token.
    created_at: datetime | None = None # set in DB when creating a message.
    
class Conversation(BaseModel):
    id: int
    name: str

    @classmethod
    def from_query_result(cls, id, name):
        return cls(
            id=id,
            name=name
        )

class CreateConversation(BaseModel):
    name: str
    user_ids: list[int]
    
class UserConversation(BaseModel):
    username: str
    
class Category(BaseModel):
    id: int
    name: str
    is_private: int  # 0 or 1
    is_locked: int  # same 0 or 1

class CategoryUserAccess(BaseModel):
    categories_id: int
    users_id: int
    has_right_access: int # 0 or 1