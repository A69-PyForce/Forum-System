from tempfile import template
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from services import conversations_service, users_service
from common import authenticate
from data.models import Name, Message, CreateConversation
import utils.auth_utils as auth_utils

conversations_router = APIRouter(prefix="/conversations")
templates = CustomJinja2Templates(directory="templates")

@conversations_router.get("/")
def get_all_conversations(request: Request, contains_user: str | None = None):
    
    auth_user = authenticate.get_user_if_token(request)
    if not auth_user:
        return RedirectResponse("/users/login", status_code=302)
    
    user_ids = set()
    user_ids.add(auth_user.id)
    
    if contains_user:
        user = users_service.find_user_by_username(contains_user)
        if user: user_ids.add(user.id)
    
    conversations = conversations_service.get_all_conversations(user_ids)
    
    return templates.TemplateResponse(
        "conversations_list.html",
        {"request": request, "user": auth_user, "conversations": conversations}
    )
    
@conversations_router.get("/{conversation_id}")
def get_conversation(conversation_id: int, request: Request):
    
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("users/login", status_code=302)
    
    conversation = conversations_service.get_conversation(conversation_id)
    
    if not conversation or not conversations_service.is_user_in_conversation(user.id, conversation_id):
        return RedirectResponse("/conversations", status_code=302)
    
    return templates.TemplateResponse(
        "conversation_detail.html",
        {"request": request, "user": user, "conversation": conversation}
    )
    
@conversations_router.post("/")
def create_conversation(request: Request, name: str = Form(...), participants: list[str] = Form(default=[])):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    user_ids = set()
    user_ids.add(user.id)
    
    # Find user IDS for all participant usernames
    for username in participants:
        participant = users_service.find_user_by_username(username)
        if participant:
            user_ids.add(participant.id)
            
    # Create the conversation
    conversation = conversations_service.create_conversation(name, user_ids)
    if not conversation:
        # Optionally, render a template with an error message
        return templates.TemplateResponse(
            "conversations_list.html",
            {"request": request, "user": user, "conversations": conversations_service.get_all_conversations({user.id}), "error": "Could not create conversation."}
        )

    return RedirectResponse(f"/conversations/{conversation.id}", status_code=302)
    
@conversations_router.post("/{conversation_id}")
def create_message_in_conversation(conversation_id: int, request: Request, text: str = Form(...)):
    
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    message = Message(
        text=text, conversation_id=conversation_id, sender_id=user.id
    )
    conversations_service.create_new_message(message)
    
    return RedirectResponse(f"/conversations/{conversation_id}", status_code=302)

@conversations_router.post("/{conversation_id}/add_user")
def add_user_to_conversation(conversation_id: int, request: Request, username: str = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    target_user = users_service.find_user_by_username(username)
    if target_user:
        if conversations_service.add_user_to_conversation(target_user.id, conversation_id):
            message = Message(
                text=f"* {user.username} added {target_user.username} to this conversation *", 
                conversation_id=conversation_id, sender_id=user.id
            )
            conversations_service.create_new_message(message)
        
    return RedirectResponse(f"/conversations/{conversation_id}", status_code=302)

@conversations_router.post("/{conversation_id}/remove_user")
def add_user_to_conversation(conversation_id: int, request: Request, username: str = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    target_user = users_service.find_user_by_username(username)
    if target_user:
        if conversations_service.remove_user_from_conversation(target_user.id, conversation_id):
            message = Message(
                text=f"* {user.username} removed {target_user.username} from this conversation *", 
                conversation_id=conversation_id, sender_id=user.id
            )
            conversations_service.create_new_message(message)
        
    return RedirectResponse(f"/conversations/{conversation_id}", status_code=302)

