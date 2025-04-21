import sys
from pathlib import Path

# Add the parent directory of main-repo to the Python path
# Allows imports from other folders
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.database import insert_query
from data.models import Message

def create_new_message(message_data: Message) -> bool:
    """Create a new message from message data. Return the True if successful, False otherwise."""
    last_row_id = insert_query("INSERT INTO messages(text, sender_id, receiver_id) VALUES (?, ?, ?)",
    (message_data.text, message_data.sender_id, message_data.receiver_id,))
    return True if last_row_id else False