from datetime import datetime, timezone
from data.database import read_query, insert_query
from data.models import Reply, ReplyCreate


def get_by_topic(topics_id: int):
    sql = """
    SELECT r.id, r.text, r.topic_id, r.user_id, r.created_at, u.username
    FROM replies r
    JOIN users u ON r.user_id = u.id
    WHERE r.topic_id = ?
    ORDER BY r.created_at ASC
    """
    data = read_query(sql, (topics_id,))
    return [Reply.from_query_result(*row) for row in data]

def create(reply_data: ReplyCreate, user_id: int, topic_id: int):
    sql = """INSERT INTO replies ( text, topic_id, user_id, created_at) VALUES (?, ?, ?, ?)"""

    now = datetime.now(timezone.utc)

    new_id = insert_query(sql,(reply_data.text, topic_id, user_id, now))

    if not new_id:
        return None

    return Reply.from_query_result(new_id, reply_data.text, topic_id, user_id, now)

def exists(reply_id: int):
    return any(read_query("""SELECT 1 FROM replies WHERE id = ?""",(reply_id,)))


def get_by_id(reply_id):
    data = read_query(
        """SELECT id, text, topic_id, user_id, created_at
            FROM replies 
            WHERE id = ?""", (reply_id,))

    return next((Reply.from_query_result(*row) for row in data), None)