from pydantic import BaseModel, StringConstraints, field_validator
from typing import Annotated


class UserLoginData(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int | None = None
    username: Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9]+$')] # Only letters, numbers and no special characters for usernames.
    password: str
    is_admin: int # we are using tinyint which is 0 and 1 for true or false ?
    # will Pydantic automatically - converts it to true or False
    @classmethod
    def from_query_result(cls, id, username, password, is_admin):
        return cls(
            id=id,
            username=username,
            password=password,
            is_admin=is_admin
        )
    # def is_admin(self):
    #     return self.role == 'Admin'

class CategoryCreate(BaseModel):
    name: str

class Category(BaseModel):
    id: int | None
    name: str
    is_private: int  # 0 or 1
    is_locked: int  # same 0 or 1

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

class MessageCreate(BaseModel):
    text: str
    receiver_id: int

class Message(BaseModel):
    id: int | None
    text: str
    sender_id: int
    receiver_id: int

    @classmethod
    def from_query_result(cls, id: int, text: str, sender_id: int, receiver_id: int) -> "Message":
        return cls(
            id=id,
            text=text,
            sender_id=sender_id,
            receiver_id=receiver_id)

# class Token(BaseModel):
#     access_token: str
#     token_type: str # automatic documentation and validation of the answer

class CategoryUserAccess(BaseModel):
    categories_id: int
    users_id: int
    has_right_access: int # 0 or 1

class Vote(BaseModel):
    id: int | None
    reply_id: int
    users_id: int