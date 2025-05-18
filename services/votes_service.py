from data.database import read_query, insert_query, update_query
from data.models import Vote


def vote(reply_id: int, user_id: int, type_vote: str):
    """
    Create or update a user's vote on a reply.

    Each user can have only one vote (up or down) per reply:
      - If the vote does not exist, insert a new vote.
      - If the same vote type already exists, return the existing vote.
      - If the vote exists but is a different type, update it.

    Args:
        reply_id (int): The ID of the reply being voted on.
        user_id (int): The ID of the user casting the vote.
        type_vote (str): The type of vote ("up" or "down").

    Returns:
        Vote: The created or updated Vote object.
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
    """
    Count upvotes and downvotes for all replies in a topic.

    Args:
        topic_id (int): The ID of the topic whose replies are counted.

    Returns:
        dict[int, dict[str, int]]: A dictionary mapping reply IDs to dictionaries
        with keys 'up' and 'down', containing the respective vote counts.
        Example: { 17: {'up': 5, 'down': 2}, ... }
    """
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
