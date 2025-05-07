from data.database import read_query, insert_query
from data.models import Topic, TopicCreate


def all(search: str = None, *, limit: int = None, offset: int = None):
    """
    Retrieve all topics with optional search and pagination.

    Args:
        search (str | None): Substring to filter topics by title.
        limit (int | None): Maximum number of records to return.
        offset (int | None): Number of records to skip.

    Returns:
        Generator[Topic]: A generator yielding Topic instances.
    """
    if search is None:
        query = """
        SELECT id, title, content, categories_id, user_id, is_locked
        FROM topics"""
        params: tuple = ()

    else:
        query = """
        SELECT id, title, content, categories_id, user_id, is_locked
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
    Sort a list of Topic instances by a given attribute.

    Args:
        topics (list[Topic]): List of topics to sort.
        attribute (str): Attribute name to sort by ('title', 'content', or 'id').
        reverse (bool): Whether to sort in descending order.

    Returns:
        list[Topic]: Sorted list of Topic instances.
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
    Retrieve a single topic by its ID.

    Args:
        id (int): The ID of the topic to fetch.

    Returns:
        Topic | None: The Topic instance if found, else None.
    """
    data = read_query(
        """SELECT id, title, content, categories_id, user_id, is_locked
            FROM topics 
            WHERE id = ?""", (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


def create(topic: TopicCreate, user_id: int):
    """
    Create a new topic record in the database.

    Args:
        topic (TopicCreate): Model containing title, content, and categories_id.
        user_id (int): ID of the user creating the topic.

    Returns:
        Topic | None: The newly created Topic instance, or None on failure.
    """
    new_id = insert_query(
        'INSERT INTO topics(title ,content , categories_id, user_id, is_locked) VALUES(?,?,?,?,?)',
        (topic.title, topic.content, topic.categories_id, user_id, 0))

    if not new_id:
        return None

    return Topic.from_query_result(
        new_id,
        topic.title,
        topic.content,
        topic.categories_id,
        user_id,
        0
    )