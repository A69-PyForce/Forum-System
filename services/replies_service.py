from data.database import read_query
from data.models import Reply


def get_by_topic(topics_id: int):
    data = read_query(
        '''SELECT id, text, topics_id, user_id
            FROM replies 
            WHERE topics_id = ?''', (topics_id,))

    return (Reply.from_query_result(*row) for row in data)
