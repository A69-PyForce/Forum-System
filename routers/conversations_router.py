from fastapi import APIRouter, Header, Response, HTTPException
from common import responses, authenticate
from data.models import Message, CreateConversation, UserConversation, User, Conversation
import services.conversations_service as conversation_service
import services.users_service as user_service

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

conversation_router = APIRouter(prefix='/conversations')

@conversation_router.post('/')
def create_conversation(c_data: CreateConversation):
    
    # Verify that all users exist
    for id in c_data.user_ids:
        if not user_service.find_user_by_id(id): return responses.NotFound(f"User with id {id} not found.")
        
    conversation = conversation_service.create_conversation(c_data.name, c_data.user_ids)
    if not conversation: return responses.BadRequest("Error creating conversation.")
    return conversation

@conversation_router.post('/{conversation_id}')
def create_message_in_conversation(conversation_id: int, message_data: Message, u_token: str = Header()):
    
    # Validate input params
    auth_user, _ = _generic_validator(u_token, conversation_id)
    
    # Set the sender_id in message_data to match the one from the auth_user
    message_data.sender_id = auth_user.id
    
    # Set the conversation_id in message_data to match the one from the conversation.id
    message_data.conversation_id = conversation_id
    
    # If all checks are passed, create the message
    if conversation_service.create_new_message(message_data):
        return responses.Created("Message successfully created.")
    
    return responses.InternalServerError("Message not created.")

@conversation_router.put('/{conversation_id}/users')
def add_user_to_conversation(conversation_id: int, user_conv: UserConversation, u_token: str = Header()):
    
    # Validate input params
    _, conversation = _generic_validator(u_token, conversation_id)
    
    # Try to find user by username
    user = user_service.find_user_by_username(user_conv.username)
    if not user: return responses.NotFound(f"User with name '{user_conv.username}' not found.")
    
    # Try to add user to conversation
    if conversation_service.add_user_to_conversation(user.id, conversation.id):
        return responses.Created(f"User with name '{user.username}' added successfuly.")
    
    return responses.InternalServerError(f"User with name '{user.username}' not added.")

@conversation_router.delete('/{conversation_id}/users')
def remove_user_from_conversation(conversation_id: int, user_conv: UserConversation, u_token: str = Header()):
    
    # Validate input params
    _, conversation = _generic_validator(u_token, conversation_id)
    
    # Try to find user by username
    user = user_service.find_user_by_username(user_conv.username)
    if not user: return responses.NotFound(f"User with name '{user_conv.username}' not found.")
    
    # Try to remove user from conversation
    if conversation_service.remove_user_from_conversation(user.id, conversation.id):
        return responses.Created(f"User with name '{user_conv.username}' removed successfuly.")
    
    return responses.InternalServerError(f"User with name '{user_conv.username}' not removed.")
    

@conversation_router.get('/{conversation_id}')
def get_conversation(conversation_id: int, u_token: str = Header()):
    
    # Validate input params
    _generic_validator(u_token, conversation_id)
    
    # Try to view conversation
    conversation = conversation_service.get_conversation(conversation_id)
    if not conversation: return responses.NotFound(f"Conversation with id {conversation_id} not found.")

    return conversation

@conversation_router.get('/')
def get_all_conversations(contains_user: str | None = None, u_token: str = Header()):
    
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