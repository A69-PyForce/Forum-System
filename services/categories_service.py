from data.database import read_query
from data.models import Category, Topic, TopicCreate


def all():
    """
    Retrieve all category records from the database.

    Returns:
        Generator[Category]: A generator yielding Category instances.
    """
    sql = """
      SELECT id, name, is_private, is_locked
        FROM categories
    """

    rows = read_query(sql)
    return (Category.from_query_result(*row) for row in rows)

def topics_by_category(
        category_id: int,
        search: str | None = None,
        *,
        limit: int | None = None,
        offset: int | None = None):
    """
    Retrieve topics for a specific category with optional search filter and pagination.

    Args:
        category_id (int): ID of the category.
        search (str | None): Substring to filter topics by title.
        limit (int | None): Maximum number of records to return.
        offset (int | None): Number of records to skip.

    Returns:
        Generator[Topic]: A generator yielding Topic instances.
    """
    if search is None:
        sql = """
        SELECT id, title, content, categories_id, user_id, is_locked
        FROM topics
        WHERE categories_id = ?"""
        params: tuple = (category_id,)

    else:
        sql = """
        SELECT id, title, content, categories_id, user_id, is_locked
        FROM topics
        WHERE categories_id = ?
        AND title LIKE ?"""
        params = (category_id, f"%{search}%")


    if limit is not None and offset is not None:
        sql += " LIMIT ? OFFSET ?"
        params += (limit, offset)

    rows = read_query(sql, params)
    return (Topic.from_query_result(*row) for row in rows)

def exists(id: int):
    """
    Check if a category exists by ID.

    Args:
        id (int): The ID of the category to check.

    Returns:
        bool: True if the category exists, False otherwise.
    """
    return any(
        read_query(
            'select id, name, is_private, is_locked from categories where id = ?',
            (id,)))