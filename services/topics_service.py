from data.database import read_query, insert_query, update_query
from data.models import Topic, TopicCreate


def all(search: str = None, *, limit: int = None, offset: int = None):
    """
    Retrieve all topics, with optional search by title and pagination.

    Args:
        search (str | None): Substring to filter topics by title.
        limit (int | None): Maximum number of topics to return.
        offset (int | None): Number of topics to skip (for pagination).

    Returns:
        Generator[Topic]: A generator yielding Topic instances from the database.
    """
    if search is None:
        query = """
        SELECT id, title, content, category_id, user_id, is_locked, best_reply_id, created_at
        FROM topics"""
        params: tuple = ()

    else:
        query = """
        SELECT id, title, content, category_id, user_id, is_locked, best_reply_id, created_at
        FROM topics
        WHERE title LIKE ?"""

        params = (f"%{search}%",)

    if limit is not None and offset is not None:
        query += " LIMIT ? OFFSET ?"
        params += (limit, offset)

    data = read_query(query, params)
    return (Topic.from_query_result(*row) for row in data)


def sort(topics: list[Topic], *, attribute="title", reverse=False):
    """
    Sort a list of topics by a given attribute.

    Args:
        topics (list[Topic]): List of topics to sort.
        attribute (str): Attribute to sort by ('title', 'content', 'id'). Defaults to 'title'.
        reverse (bool): Whether to sort in descending order. Defaults to False.

    Returns:
        list[Topic]: A sorted list of topics.
    """
    if attribute == "title":
        sort_fn = lambda t: t.title
    elif attribute == "content":
        sort_fn = lambda t: t.content
    else:
        sort_fn = lambda t: t.id

    return sorted(topics, key=sort_fn, reverse=reverse)


def get_by_id(id: int):
    """
    Retrieve a topic from the database by its unique ID.

    Args:
        id (int): Unique identifier for the topic.

    Returns:
        Topic | None: The Topic instance if found, else None.
    """
    data = read_query(
        """SELECT id, title, content, category_id, user_id, is_locked, best_reply_id, created_at
            FROM topics 
            WHERE id = ?""", (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


def create(topic: TopicCreate, user_id: int):
    """
    Create a new topic in the database.

    Args:
        topic (TopicCreate): Pydantic model containing the title, content, and category_id.
        user_id (int): ID of the user creating the topic.

    Returns:
        Topic | None: The newly created Topic instance if successful, or None on failure.
    """
    new_id = insert_query(
        'INSERT INTO topics(title ,content , category_id, user_id, is_locked) VALUES(?,?,?,?,?)',
        (topic.title, topic.content, topic.category_id, user_id, 0))

    if not new_id:
        return None
    
    return Topic(
        id=new_id,
        title=topic.title,
        content=topic.content,
        category_id=topic.category_id,
        user_id=user_id,
        is_locked=0,
        best_reply_id=None
    )

def select_best_reply(topic_id: int, reply_id: int) -> bool:
    """
    Mark a specific reply as the 'best reply' for a topic.

    Args:
        topic_id (int): ID of the topic.
        reply_id (int): ID of the reply to mark as best.

    Returns:
        bool: True if the update succeeded (row was changed), False otherwise.
    """
    sql = "UPDATE topics SET best_reply_id = ? WHERE id = ?"
    return update_query(sql, (reply_id, topic_id)) > 0

def set_locked(topic_id: int, locked: bool) -> bool:
    """
    Set the is_locked flag for a topic (lock or unlock the topic).

    Args:
        topic_id (int): ID of the topic.
        locked (bool): True to lock, False to unlock.

    Returns:
        bool: True if the update affected one row, False otherwise.
    """
    sql = "UPDATE topics SET is_locked = ? WHERE id = ?"
    return update_query(sql, (1 if locked else 0, topic_id)) == 1

def toggle_lock(topic_id: int) -> bool:
    """
    Toggle the lock status of a topic (locked/unlocked).

    Args:
        topic_id (int): ID of the topic.

    Returns:
        bool: True if the lock status was toggled successfully, False otherwise.
    """
    result = read_query("SELECT is_locked FROM topics WHERE id = ?", (topic_id,))
    if not result:
        return False

    current_status = result[0][0]
    return set_locked(topic_id, not current_status)