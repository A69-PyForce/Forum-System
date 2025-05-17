from data.database import insert_query, read_query, update_query
from mariadb import IntegrityError
from data.models import *

def create_new_message(message_data: Message) -> bool:
    """
    Create a new message in the database.

    Args:
        message_data (Message): The message data to insert.

    Returns:
        bool: True if the message was created successfully, False otherwise.
    """
    query = '''INSERT INTO messages(text, conversation_id, sender_id)
               VALUES(?, ?, ?)'''

    last_row_id = insert_query(
        query, (message_data.text, message_data.conversation_id, message_data.sender_id,)
    )
    
    return True if last_row_id else False

def create_conversation(conversation_name: str, user_ids: list[int]) -> CreateConversationResponse | None:
    """
    Create a new conversation with the given name and participants.

    Args:
        conversation_name (str): The name of the conversation.
        user_ids (list[int]): List of user IDs to add to the conversation.

    Returns:
        CreateConversationResponse: The created conversation data if successful.
        None: If creation failed.
    """
    if len(user_ids) < 1: return None
    
    # Create a new conversation in conversations table
    query = "INSERT INTO conversations(name) VALUES (?)"
    conversation_id = insert_query(query, (conversation_name,))
    
    if not conversation_id: return None
    
    # Update conversations_has_users table
    query = "INSERT INTO conversations_has_users(conversation_id, user_id) VALUES (?, ?)"
    for id in user_ids: insert_query(query, (conversation_id, id,))

    return CreateConversationResponse.from_query_result(id=conversation_id, name=conversation_name, user_ids=user_ids)

def add_user_to_conversation(user_id: int, conversation_id: int) -> bool:
    """
    Add a user to a conversation.

    Args:
        user_id (int): The ID of the user to add.
        conversation_id (int): The ID of the conversation.

    Returns:
        bool: True if the user was added successfully, False otherwise.
    """
    query = "INSERT INTO conversations_has_users(user_id, conversation_id) VALUES (?, ?)"
    try:
        return update_query(query, (user_id, conversation_id,))
    except IntegrityError:
        return False

def remove_user_from_conversation(user_id: int, conversation_id: int) -> bool:
    """
    Remove a user from a conversation.

    Args:
        user_id (int): The ID of the user to remove.
        conversation_id (int): The ID of the conversation.

    Returns:
        bool: True if the user was removed successfully, False otherwise.
    """
    query = "DELETE FROM conversations_has_users WHERE user_id = ? AND conversation_id = ?"
    return update_query(query, (user_id, conversation_id,))
     
def find_conversation_by_id(conversation_id: int) -> Conversation | None:
    """
    Find a conversation by its ID.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        Conversation: The conversation object if found.
        None: If not found.
    """
    query = "SELECT * FROM conversations WHERE id = ?"
    data = read_query(query, (conversation_id,))
    return next((Conversation.from_query_result(*row) for row in data), None)
    
def is_user_in_conversation(user_id: int, conversation_id: int) -> bool:
    """
    Check if a user is a participant in a conversation.

    Args:
        user_id (int): The user ID.
        conversation_id (int): The conversation ID.

    Returns:
        bool: True if the user is in the conversation, False otherwise.
    """
    query = '''SELECT * FROM conversations_has_users
               WHERE user_id = ? AND conversation_id = ?'''
    
    data = read_query(query, (user_id, conversation_id,))
    return True if data else False

def get_conversation(conversation_id: int) -> ConversationResponse | None:
    """
    Retrieve a conversation and its messages by conversation ID.

    Args:
        conversation_id (int): The ID of the conversation.

    Returns:
        ConversationResponse: The conversation data with messages if found.
        None: If not found.
    """
    # Try to find conversation
    conversation_data = read_query("SELECT id, name FROM conversations WHERE id = ?", (conversation_id,))
    if not conversation_data: return None
    
    # Get message data
    query = '''SELECT m.text, u.username, u.avatar_url, m.created_at
               FROM messages AS m
               JOIN users AS u ON m.sender_id = u.id
               WHERE m.conversation_id = ?
               ORDER BY m.created_at ASC'''
               
    messages_data = read_query(query, (conversation_id,))
    messages = (MessageResponse.from_query_result(*row) for row in messages_data)
    
    return ConversationResponse.from_query_result(
        id=conversation_data[0][0],
        name=conversation_data[0][1],
        messages=messages
    )
    
def get_all_conversations(user_ids: set[int]) -> list[AllConversationsResponse] | None:
    """
    Get all conversations that contain the given user IDs.

    Args:
        user_ids (set[int]): Set of user IDs to filter conversations.

    Returns:
        list[AllConversationsResponse]: List of conversations with participants.
        None: If no conversations are found.
    """
    # Convert user ids list to comma-separated string for the query
    placeholders = ", ".join(["?"] * len(user_ids))
    
    # Get conversation ids
    query = f"""
    SELECT c.id, c.name
    FROM conversations AS c
    JOIN conversations_has_users AS chu 
    ON c.id = chu.conversation_id
    WHERE chu.user_id IN ({placeholders})
    GROUP BY c.id, c.name
    HAVING COUNT(DISTINCT chu.user_id) = ?"""
               
    # Add the count of user_ids as the last parameter
    params = tuple(user_ids) + (len(user_ids),)
    conversations_data = read_query(query, params)
    if not conversations_data: return None
    
    results = []
    for conv_id, conv_name in conversations_data:
        
        # Query to get all participants for this conversation
        
        participants_query = """
        SELECT u.id, u.username
        FROM users AS u
        JOIN conversations_has_users AS chu
        ON u.id = chu.user_id
        WHERE chu.conversation_id = ?
        ORDER BY u.username"""
                                
        participants_data = read_query(participants_query, (conv_id,))
        participants = (ParticipantsResponse.from_query_result(*row) for row in participants_data)
        
        results.append(AllConversationsResponse.from_query_result(id=conv_id, name=conv_name, participants=participants))
    
    return results
    
    
    