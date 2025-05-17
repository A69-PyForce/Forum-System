from data.database import read_query, insert_query, update_query
from data.models import Category, Topic


def all():
    """
    Retrieve all category records from the database.

    Returns:
        Generator[Category]: A generator yielding Category instances.
    """
    sql = """
      SELECT id, name, is_private, is_locked, image_url
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
        SELECT id, title, content, category_id, user_id, is_locked, best_reply_id, created_at
        FROM topics
        WHERE category_id = ?"""
        params: tuple = (category_id,)

    else:
        sql = """
        SELECT id, title, content, category_id, user_id, is_locked, best_reply_id, created_at
        FROM topics
        WHERE  = ?
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


def get_by_id(category_id: int):
    data = read_query(
        """SELECT id, name, is_private, is_locked, image_url
            FROM categories 
            WHERE id = ?""", (category_id,))

    return next((Category.from_query_result(*row) for row in data), None)

def create(name: str) -> Category:
    sql = """INSERT INTO categories (name, is_private, is_locked)VALUES(?, 0, 0)"""
    new_id = insert_query(sql, (name,))

    return Category.from_query_result(id=new_id, name=name, is_private=0, is_locked=0)

def set_privacy(category_id: int, is_private: bool) -> bool:
    sql = """UPDATE categories SET is_private = ? WHERE id = ?"""
    rows = update_query(sql, (1 if is_private else 0, category_id))
    return rows == 1

def set_locked(category_id: int, locked: bool) -> bool:
    """
    Set the is_locked flag on a category.
    Returns True if exactly one row was updated.
    """
    sql = "UPDATE categories SET is_locked = ? WHERE id = ?"
    return update_query(sql, (1 if locked else 0, category_id)) == 1

def update_category_image_url(category_id: int, image_url: str) -> bool:
    return update_query(
        "UPDATE categories SET image_url = ? WHERE id = ?", (image_url, category_id)
    )