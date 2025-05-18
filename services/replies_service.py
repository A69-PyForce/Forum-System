from datetime import datetime, timezone
from data.database import read_query, insert_query
from data.models import Reply, ReplyCreate


def get_by_topic(topics_id: int):
    """
    Retrieve all replies for a specific topic, including author information.

    Args:
        topics_id (int): The ID of the topic whose replies are fetched.

    Returns:
        list[Reply]: A list of Reply objects for the given topic, ordered by creation time (ascending).
    """
    sql = """
    SELECT r.id, r.text, r.topic_id, r.user_id, r.created_at, u.username, u.avatar_url
    FROM replies r
    JOIN users u ON r.user_id = u.id
    WHERE r.topic_id = ?
    ORDER BY r.created_at ASC
    """
    data = read_query(sql, (topics_id,))
    return [Reply.from_query_result(*row) for row in data]

def create(reply_data: ReplyCreate, user_id: int, topic_id: int):
    """
    Create a new reply for a given topic and user.

    Args:
        reply_data (ReplyCreate): Data for the new reply (text).
        user_id (int): ID of the user posting the reply.
        topic_id (int): ID of the topic to which the reply belongs.

    Returns:
        bool: True if the reply was successfully created, False otherwise.
    """
    sql = """INSERT INTO replies (text, topic_id, user_id) VALUES (?, ?, ?)"""

    new_id = insert_query(sql,(reply_data.text, topic_id, user_id))
    return True if new_id else False

def exists(reply_id: int):
    """
    Check if a reply exists by its ID.

    Args:
        reply_id (int): The ID of the reply to check.

    Returns:
        bool: True if the reply exists, False otherwise.
    """
    return any(read_query("""SELECT 1 FROM replies WHERE id = ?""",(reply_id,)))


def get_by_id(reply_id):
    """
    Retrieve a reply by its ID.

    Args:
        reply_id (int): The unique identifier of the reply.

    Returns:
        Reply | None: The Reply object if found, otherwise None.
    """
    data = read_query(
        """SELECT id, text, topic_id, user_id, created_at
            FROM replies 
            WHERE id = ?""", (reply_id,))

    return next((Reply.from_query_result(*row) for row in data), None)