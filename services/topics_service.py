from data.database import read_query
from data.models import Topic


def all(search: str = None, *, limit: int = None, offset: int = None):
    if search is None:
        sql = """
            SELECT id, title, content, categories_id, user_id, is_locked
              FROM topics
        """
        params: tuple = ()
    else:
        sql = """
            SELECT id, title, content, categories_id, user_id, is_locked
              FROM topics
             WHERE title LIKE ?
        """
        params = (f"%{search}%",)

    if limit is not None and offset is not None:
        sql += " LIMIT ? OFFSET ?"
        params += (limit, offset)

    data = read_query(sql, params)
    return (Topic.from_query_result(*row) for row in data)


def sort(topics: list[Topic], *, attribute="title", reverse=False):
    if attribute == "title":
        sort_fn = lambda t: t.title
    elif attribute == "content":
        sort_fn = lambda t: t.content
    else:
        sort_fn = lambda t: t.id

    return sorted(topics, key=sort_fn, reverse=reverse)


def get_by_id(id: int):
    data = read_query(
        """SELECT id, title, content, categories_id, user_id, is_locked
            FROM topics 
            WHERE id = ?""", (id,))
# to implement list of Reply resources
    return next((Topic.from_query_result(*row) for row in data), None)