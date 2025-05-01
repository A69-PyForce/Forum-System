from data.database import read_query
from data.models import Category


def all():
    sql = """
      SELECT id, name, is_private, is_locked
        FROM categories
    """

    rows = read_query(sql)
    return (Category.from_query_result(*row) for row in rows)