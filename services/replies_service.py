from datetime import datetime, timezone


from data.database import read_query, insert_query
from data.models import Reply, ReplyCreate


def get_by_topic(topics_id: int):
    """
    Retrieve all replies for a given topic ID.

    Args:
        topics_id (int): The ID of the topic whose replies are fetched.

    Returns:
        Generator[Reply]: A generator yielding Reply instances.
    """
    data = read_query(
        '''SELECT id, text, topic_id, user_id, created_at
            FROM replies 
            WHERE topic_id = ?''', (topics_id,))

    return (Reply.from_query_result(*row) for row in data)

def create(reply_data: ReplyCreate, user_id: int, topic_id: int):
    sql = """INSERT INTO replies ( text, topic_id, user_id, created_at) VALUES (?, ?, ?, ?)"""

    now = datetime.now(timezone.utc)

    new_id = insert_query(sql,(reply_data.text, topic_id, user_id, now))

    if not new_id:
        return None

    return Reply.from_query_result(new_id, reply_data.text, topic_id, user_id, now)