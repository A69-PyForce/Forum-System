from data.database import read_query
from data.models import Category, Topic


def all():
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

    # row = next(read_query(
    #     "SELECT id, name, is_private, is_locked FROM categories WHERE id = ?",
    #     (category_id,)), None)
    # if row is None:
    #     return None
    # category = CategoryWithTopics.from_query_result(*row)
    #
    # category.topics = list(
    #     topics_service.all(search=search, category_id=category_id, limit=limit, offset=offset))
    # return category