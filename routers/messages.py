from fastapi import APIRouter, Header
from common import responses, authenticate
from data.models import Message
import services.message_service as message_service
import services.user_service as user_service

message_router = APIRouter(prefix='/messages')

@message_router.post('/{username}/send')
def create_message(username: str, message_data: Message, u_token: str = Header()):
        
    # Authenticate and get user from token
    auth_user = authenticate.get_user_or_raise_401(u_token)
    
    # Ensure the username in the url matches token
    if auth_user.username != username or message_data.sender_id != auth_user.id:
        return responses.BadRequest("Sender missmatch or unauthorized.")
    
    # Check if the receiver exists
    receiver_user = user_service.find_user_by_id(message_data.receiver_id)
    if not receiver_user:
        return responses.BadRequest("Receiver not found.")
    
    # Create the message
    is_created = message_service.create_new_message(message_data)
    if is_created:
        return {"message": "Message created."}
    return responses.BadRequest("Failed to create message.")

