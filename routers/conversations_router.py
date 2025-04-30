import services.conversations_service as conversation_service
from fastapi import APIRouter, Header, HTTPException
import services.users_service as user_service
from common import responses, authenticate
from data.models import *

def _generic_validator(u_token: str, conversation_id: int) -> tuple[User, Conversation]:
    """Helper function for validating that the user from given token belongs to the conversation from the given id."""
    
    # Authenticate and get user from token
    auth_user = authenticate.get_user_or_raise_401(u_token)
    
    # Try to find conversation by id
    conversation = conversation_service.find_conversation_by_id(conversation_id)
    if not conversation: raise HTTPException(detail=f"Conversation with id {conversation_id} not found.", status_code=404)
    
    # Verify that user from token belongs in conversation from id
    if not conversation_service.is_user_in_conversation(auth_user.id, conversation.id):
        raise HTTPException(detail=f"User '{auth_user.username}' does not belong in this conversation.", status_code=401)
    
    return auth_user, conversation

# ------------------------ CONVERSATIONS ROUTER BEGIN -------------------------

conversation_router = APIRouter(prefix='/conversations')

# -----------------------------------------------------------------------------
# CONVERSATIONS - GET REQUESTS
# -----------------------------------------------------------------------------

@conversation_router.get('/')
def get_all_conversations(contains_user: str | None = None, u_token: str = Header()) -> list[AllConversationsResponse]:
    
    # List for filtering conversations
    user_ids = set()
    
    # Validate user token
    auth_user = authenticate.get_user_or_raise_401(u_token)
    user_ids.add(auth_user.id)
    
    # Try to get id from contains_user query parameter
    if contains_user:
        user = user_service.find_user_by_username(contains_user)
        if not user: return responses.NotFound(f"No conversations of user '{auth_user.username}' found.")
        user_ids.add(user.id)
    
    conversations = conversation_service.get_all_conversations(user_ids)
    if not conversations: return responses.NotFound(f"No conversations of user '{auth_user.username}' found.")
    
    return conversations

@conversation_router.get('/{conversation_id}')
def get_conversation(conversation_id: int, u_token: str = Header()) -> ConversationResponse:
    
    # Validate input params
    _generic_validator(u_token, conversation_id)
    
    # Try to view conversation
    conversation = conversation_service.get_conversation(conversation_id)
    if not conversation: return responses.NotFound(f"Conversation with id {conversation_id} not found.")

    return conversation

# -----------------------------------------------------------------------------
# CONVERSATIONS - POST REQUESTS
# -----------------------------------------------------------------------------

@conversation_router.post('/')
def create_conversation(conv_data: CreateConversation, u_token = Header(), create_with: int | None = None) -> CreateConversationResponse:
    
    auth_user = authenticate.get_user_or_raise_401(u_token)
    
    # Create a set of user ids
    user_ids = set()
    if conv_data.user_ids: 
        for id in conv_data.user_ids: user_ids.add(id)
    if create_with: 
        user_ids.add(create_with)
    user_ids.add(auth_user.id)
    
    # Verify that all users exist
    for id in user_ids:
        if not user_service.find_user_by_id(id): return responses.NotFound(f"User with id {id} not found.")
        
    conversation = conversation_service.create_conversation(conv_data.name, user_ids)
    if not conversation: return responses.BadRequest("Error creating conversation.")
    return conversation

@conversation_router.post('/{conversation_id}')
def create_message_in_conversation(conversation_id: int, message_data: CreateMessage, u_token: str = Header()):
    
    # Validate input params
    auth_user, _ = _generic_validator(u_token, conversation_id)
    
    # Create a Message
    message = Message(text=message_data.text, conversation_id=conversation_id, sender_id=auth_user.id)
    if conversation_service.create_new_message(message):
        return responses.Created("Message send.")
    
    return responses.InternalServerError("Message not send.")

# -----------------------------------------------------------------------------
# CONVERSATIONS - PUT REQUESTS
# -----------------------------------------------------------------------------

@conversation_router.put('/{conversation_id}/users')
def add_user_to_conversation(conversation_id: int, username: Name, u_token: str = Header()):
    
    # Validate input params
    _, conversation = _generic_validator(u_token, conversation_id)
    
    # Try to find user by username
    user = user_service.find_user_by_username(username.name)
    if not user: return responses.NotFound(f"User with name '{username.name}' not found.")
    
    # Check if user is already in conversation
    if conversation_service.is_user_in_conversation(user.id, conversation.id):
        return responses.BadRequest(f"User with name '{username.name}' is already in this conversation.")
    
    # Try to add user to conversation
    if conversation_service.add_user_to_conversation(user.id, conversation.id):
        return responses.Created(f"User with name '{user.username}' added successfuly.")
    
    return responses.InternalServerError(f"User with name '{user.username}' not added.")

# -----------------------------------------------------------------------------
# CONVERSATIONS - DELETE REQUESTS
# -----------------------------------------------------------------------------

@conversation_router.delete('/{conversation_id}/users')
def remove_user_from_conversation(conversation_id: int, username: Name, u_token: str = Header()):
    
    # Validate input params
    _, conversation = _generic_validator(u_token, conversation_id)
    
    # Try to find user by username
    user = user_service.find_user_by_username(username.name)
    if not user: return responses.NotFound(f"User with name '{username.name}' not found.")
    
    # Try to remove user from conversation
    if conversation_service.remove_user_from_conversation(user.id, conversation.id):
        return responses.Created(f"User with name '{username.name}' removed successfuly.")
    
    return responses.InternalServerError(f"User with name '{username.name}' not removed.")

# ------------------------- CONVERSATIONS ROUTER END -------------------------