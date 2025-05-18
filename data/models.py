from pydantic import BaseModel, StringConstraints, field_validator
from datetime import datetime
from typing import Annotated, Literal, Optional

class Username(BaseModel):
    name: str

class UserLoginData(BaseModel):
    username: str
    password: str

class UserRegisterData(BaseModel):
    
    username: Annotated[str, StringConstraints(min_length=1, max_length=45)]
    password: Annotated[str, StringConstraints(min_length=4, max_length=255)]
    is_admin: int

class User(BaseModel):
    id: int
    username: str
    password: str
    is_admin: int
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    
    @classmethod
    def from_query_result(cls, id, username, password, is_admin, avatar_url, created_at):
        return cls(
            id=id,
            username=username,
            password=password,
            is_admin=is_admin,
            avatar_url=avatar_url,
            created_at=created_at
        )

class Category(BaseModel):
    id: Optional[int] = None
    name: Annotated[str, StringConstraints(min_length=1, max_length=45)]
    is_private: int
    is_locked: int
    image_url: Optional[str] = None

    @classmethod
    def from_query_result(cls, id: int, name: str, is_private: int, is_locked: int, image_url: str | None = None):
        return cls(
            id=id,
            name=name,
            is_private=is_private,
            is_locked=is_locked,
            image_url=image_url
        )

class Topic(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    category_id: int
    user_id: int
    is_locked: int
    best_reply_id: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_query_result(cls, id, title, content, category_id, user_id, is_locked, best_reply_id, created_at) -> "Topic":
        return cls(
            id=id,
            title=title,
            content=content,
            category_id=category_id,
            user_id=user_id,
            is_locked=is_locked,
            best_reply_id=best_reply_id,
            created_at=created_at
        )

class TopicCreate(BaseModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=45)]
    content: Annotated[str, StringConstraints(min_length=1, max_length=1000)]
    category_id: int

class ReplyCreate(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1, max_length=255)]

class Reply(BaseModel):
    id: Optional[int] = None
    text: str
    topic_id: int
    user_id: int
    created_at: datetime
    username: Optional[str] = None
    avatar_url: Optional[str] = None

    @classmethod
    def from_query_result(cls, id: int, text: str, topic_id: int, user_id: int, created_at: datetime, username: Optional[str] = None, avatar_url: Optional[str] = None) -> "Reply":
        return cls(
            id=id,
            text=text,
            topic_id=topic_id,
            user_id=user_id,
            created_at=created_at,
            username=username,
            avatar_url=avatar_url
        )
        
class MessageCreate(BaseModel):
    text: Annotated[str, StringConstraints(min_length=1, max_length=255)]

class Message(BaseModel):
    id: Optional[int] = None
    text: str
    conversation_id: int
    sender_id: int
    created_at: Optional[datetime] = None
    
class MessageResponse(BaseModel):
    text: str
    username: str
    avatar_url: str | None
    created_at: datetime
    
    @classmethod
    def from_query_result(cls, text, username, avatar_url, created_at):
        return cls(
            text=text,
            username=username,
            avatar_url=avatar_url,
            created_at=created_at
        )
        
class CreateConversation(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=90)]
    user_ids: Optional[list[int]] = None
    
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

class VoteCreate(BaseModel):
    type_vote: Literal['up','down']

class Vote(BaseModel):
    id: Optional[int] = None
    reply_id: int
    user_id: int
    type_vote: str

    @classmethod
    def from_query_result(cls, id: int, reply_id: int, user_id: int, type_vote: str) -> "Vote":
        return cls(
            id=id,
            reply_id=reply_id,
            user_id=user_id,
            type_vote=type_vote
        )

class CategoryPrivacyUpdate(BaseModel):
    is_private: bool