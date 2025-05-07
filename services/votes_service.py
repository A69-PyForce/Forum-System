from data.database import read_query, insert_query, update_query
from data.models import Vote


def vote(reply_id: int, users_id: int, type_vote: str):
    """
    Creates or updates a vote. A user can only have one vote per reply.
    If the vote exists and is the same type, returns it unchanged.
    If it exists and is different, updates it.
    Otherwise, inserts a new row.
    """

    rows = read_query("SELECT id, type_vote FROM votes WHERE reply_id = ? AND users_id = ?",
        (reply_id, users_id))

    existing = next(iter(rows), None)
    if existing is None:
        new_id = insert_query(
            "INSERT INTO votes (reply_id, users_id, type_vote) VALUES (?, ?, ?)",
            (reply_id, users_id, type_vote))
        return Vote.from_query_result(new_id, reply_id, users_id, type_vote)
    else:
        vote_id, old_type = existing
        if old_type == type_vote:
            return Vote.from_query_result(vote_id, reply_id, users_id, old_type)

        update_query(
            "UPDATE votes SET type_vote = ? WHERE id = ?",
            (type_vote, vote_id))
        return Vote.from_query_result(vote_id, reply_id, users_id, type_vote)