from pydantic import BaseModel, StringConstraints, field_validator
from datetime import datetime
from typing import Annotated

class UserLoginData(BaseModel):
    username: str
    password: str

class UserRegisterData(BaseModel):
    
     # Username - Only letters, numbers and no special characters.
    username: Annotated[str, StringConstraints(pattern=r'^[a-zA-Z0-9]+$')]
    
    # Password - Must be at least 4 characters and contain at least 1 letter and 1 number.
    password: str
    @field_validator("password")
    def password_validator(cls, password: str):
        
        # Check if password is at least 4 characters long
        if not len(password) >= 4:
            raise ValueError("Password must be at least 4 characters long.")
        
        # Check if the string contains at least one digit
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number.")
        
        # Check if the string contains at least one letter
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter.")
        return password
    
    is_admin: int

class User(BaseModel):
    id: int
    username: str
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

class Name(BaseModel):
    name: str

class Message(BaseModel):
    id: int | None = None # set by db
    text: str
    conversation_id: int
    sender_id: int
    created_at: datetime | None = None # set by db
    
class MessageResponse(BaseModel):
    text: str
    username: str
    date: datetime
    
    @classmethod
    def from_query_result(cls, text, username, date):
        return cls(
            text=text,
            username=username,
            date=date
        )
        
class CreateMessage(BaseModel):
    text: str
    
class Conversation(BaseModel):
    id: int
    name: str

    @classmethod
    def from_query_result(cls, id, name):
        return cls(
            id=id,
            name=name
        )
        
class CreateConversationResponse(BaseModel):
    id: int
    name: str
    user_ids: list[int]
    
    @classmethod
    def from_query_result(cls, id, name, user_ids):
        return cls(
            id=id,
            name=name,
            user_ids=user_ids
        )
        
class ConversationResponse(BaseModel):
    id: int
    name: str
    messages: list[MessageResponse]
    
    @classmethod
    def from_query_result(cls, id, name, messages):
        return cls(
            id=id,
            name=name,
            messages=messages
        )   

class ParticipantsResponse(BaseModel):
    id: int
    name: str

    @classmethod
    def from_query_result(cls, id, name):
        return cls(
            id=id,
            name=name
        )
class AllConversationsResponse(BaseModel):
    id: int
    name: str
    participants: list[ParticipantsResponse]
    
    @classmethod
    def from_query_result(cls, id, name, participants):
        return cls(
            id=id,
            name=name,
            participants=participants
        )

class CreateConversation(BaseModel):
    name: str
    user_ids: list[int] | None = None

class CategoryUserAccess(BaseModel):
    categories_id: int
    users_id: int
    has_right_access: int # 0 or 1

class Vote(BaseModel):
    id: int | None
    reply_id: int
    users_id: int