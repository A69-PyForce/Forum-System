from data.database import read_query
from data.models import Topic


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT id, title, content, categories_id, user_id, is_locked
               FROM topics''')
    else:
        data = read_query(
            '''SELECT id, title, content, categories_id, user_id, is_locked
               FROM topics 
               WHERE title LIKE ?''', (f'%{search}%',))

    return (Topic.from_query_result(*row) for row in data)


def sort(topics: list[Topic], *, attribute='title', reverse=False):
    if attribute == 'title':
        def sort_fn(t: Topic): return t.title
    elif attribute == 'content':
        def sort_fn(t: Topic): return t.content
    else:
        def sort_fn(t: Topic): return t.id

    return sorted(topics, key=sort_fn, reverse=reverse)
