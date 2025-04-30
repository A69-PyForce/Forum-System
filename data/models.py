from pydantic import BaseModel, StringConstraints
from datetime import datetime
from typing import Annotated


class UserLoginData(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int | None = None
    username: Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9]+$')] # Only letters, numbers and no special characters for usernames.
    password: str
    is_admin: int

    @classmethod
    def from_query_result(cls, id, username, password, is_admin):
        return cls(
            id=id,
            username=username,
            password=password,
            is_admin=is_admin
        )


class CategoryCreate(BaseModel):
    name: str

class Category(BaseModel):
    id: int | None
    name: str
    is_private: int  # 0 or 1 # we are using tinyint which is 0 and 1 for true or false ?
    is_locked: int  # same 0 or 1  # will Pydantic automatically - converts it to true or False

    @classmethod
    def from_query_result(cls, id: int, name: str, is_private: int, is_locked: int):
        return cls(id=id, name=name, is_private=is_private, is_locked=is_locked)

class TopicCreate(BaseModel):
    title: str
    content: str
    category_id: int

class Topic(BaseModel):
    id: int | None
    title: str
    content: str
    category_id: int
    user_id: int
    is_locked: int

    @classmethod
    def from_query_result(cls, id: int,
                          title: str,
                          content: str,
                          category_id: int,
                          user_id: int,
                          is_locked: int) -> "Topic":
        return cls(
            id=id,
            title=title,
            content=content,
            category_id=category_id,
            user_id=user_id,
            is_locked=is_locked
        )


class ReplyCreate(BaseModel):
    text: str
    topic_id: int

class Reply(BaseModel):
    id: int | None
    text: str
    topic_id: int
    user_id: int
    votes: int
    is_best: int

    @classmethod
    def from_query_result(cls, id: int, text: str, topic_id: int, user_id: int, votes: int, is_best: int):
        return cls(
            id=id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            votes=votes,
            is_best=is_best
        )

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

class Vote(BaseModel):
    id: int | None
    reply_id: int
    users_id: int