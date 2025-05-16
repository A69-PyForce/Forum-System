from data.database import read_query, insert_query, update_query
from data.models import Vote


def vote(reply_id: int, user_id: int, type_vote: str):
    """
    Creates or updates a vote. A user can only have one vote per reply.
    If the vote exists and is the same type, returns it unchanged.
    If it exists and is different, updates it.
    Otherwise, inserts a new row.
    """

    rows = read_query("SELECT id, type_vote FROM votes WHERE reply_id = ? AND user_id = ?",
        (reply_id, user_id))

    existing = next(iter(rows), None)
    if existing is None:
        new_id = insert_query(
            "INSERT INTO votes (reply_id, user_id, type_vote) VALUES (?, ?, ?)",
            (reply_id, user_id, type_vote))
        return Vote.from_query_result(new_id, reply_id, user_id, type_vote)
    else:
        vote_id, old_type = existing
        if old_type == type_vote:
            return Vote.from_query_result(vote_id, reply_id, user_id, old_type)

        update_query(
            "UPDATE votes SET type_vote = ? WHERE id = ?",
            (type_vote, vote_id))
        return Vote.from_query_result(vote_id, reply_id, user_id, type_vote)


def count_votes_for_replies(topic_id: int) -> dict[int, dict[str, int]]:
    data = read_query("""
        SELECT r.id, 
               SUM(CASE WHEN v.type_vote = 'up' THEN 1 ELSE 0 END) as up_votes,
               SUM(CASE WHEN v.type_vote = 'down' THEN 1 ELSE 0 END) as down_votes
        FROM replies r
        LEFT JOIN votes v ON r.id = v.reply_id
        WHERE r.topic_id = ?
        GROUP BY r.id
    """, (topic_id,))

    return {reply_id: {"up": up_votes, "down": down_votes} for reply_id, up_votes, down_votes in data}
