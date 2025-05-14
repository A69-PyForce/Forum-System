from fastapi import APIRouter, Header
from pydantic import BaseModel
from common import responses
from common.authenticate import get_user_or_raise_401
from common.responses import BadRequest, InternalServerError, NotFound, Unauthorized, NoContent
from data.models import Topic, Reply, TopicCreate, ReplyCreate, Vote, VoteCreate
from services import topics_service, replies_service, categories_service, votes_service


class TopicResponseModel(BaseModel):
    """
    Response model combining a topic with its associated replies.

    Attributes:
        topic (Topic): The main topic data.
        replies (list[Reply]): List of replies to the topic.
    """
    topic: Topic
    replies: list[Reply]

class BestReplyRequest(BaseModel):
    reply_id: int

class TopicLockRequest(BaseModel):
    is_locked: bool


api_topics_router = APIRouter(prefix="/api/topics")

@api_topics_router.get("/",response_model=list[Topic])
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None,
    page: int = 1,
    size: int = 5
):
    """
    Retrieve paginated list of topics with optional filtering and sorting.

    Args:
        sort (str | None): Sort order; 'asc' or 'desc' to apply sorting by the specified attribute.
        sort_by (str | None): Attribute name to sort by (e.g., 'title', 'content').
        search (str | None): Substring to filter topics by title.
        page (int): Page number for pagination (1-indexed).
        size (int): Number of topics per page.

    Returns:
        list[Topic]: A list of Topic instances matching the given parameters.
    """
    offset = (page - 1) * size

    result = topics_service.all(search, limit=size, offset=offset)

    if sort and (sort == "asc" or sort == "desc"):
        return topics_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result


@api_topics_router.get("/{id}")
def get_topic_by_id(id: int):
    """
    Retrieve a single topic by its ID along with its replies.

    Args:
        id (int): The ID of the topic to retrieve.

    Returns:
        TopicResponseModel | JSONResponse: A TopicResponseModel if found, otherwise a NotFound response.
    """
    topic = topics_service.get_by_id(id)

    if topic is None:
        return responses.NotFound(f"Topic with ID '{id}' not found.")

    replies = list(replies_service.get_by_topic(topic.id))

    return TopicResponseModel(topic=topic,replies=replies)

@api_topics_router.post("/", status_code=201)
def create_topic(topic: TopicCreate, u_token: str = Header()):
    """
    Create a new topic under a given category, authenticated via header token.

    Args:
        topic (TopicCreate): Pydantic model containing title, content, and category_id.
        u_token (str): User authentication token passed in HTTP header.

    Returns:
        Topic | JSONResponse: The newly created Topic model, or a BadRequest response on failure.
    """
    user = get_user_or_raise_401(u_token)

    if not categories_service.exists(topic.category_id):
        return responses.BadRequest("Category does not exist.")

    if topic.title == "":
        return responses.BadRequest("Title cannot be empty.")

    if topic.content == "":
        return responses.BadRequest("Content cannot be empty.")

    category = categories_service.get_by_id(topic.category_id)
    if category.is_locked:
        return BadRequest("Category is locked. Cannot create new topics.")

    new_topic = topics_service.create(topic, user.id)
    if not new_topic:
        return responses.InternalServerError()

    return new_topic

@api_topics_router.post("/{topic_id}/replies",response_model=Reply, status_code=201)
def create_reply(topic_id: int, reply_data: ReplyCreate, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)

    if not topics_service.get_by_id(topic_id):
        return BadRequest(f"Topic with ID '{topic_id}' not found.")

    topic = topics_service.get_by_id(topic_id)
    if topic.is_locked:
        return BadRequest("Topic is locked. Cannot accept new replies.")

    new_reply = replies_service.create(reply_data, topic_id=topic_id, user_id=user.id)
    if not new_reply:
        return InternalServerError()

    return new_reply

@api_topics_router.post("/{topic_id}/replies/{reply_id}/votes",response_model=Vote)
def vote_reply(topic_id: int, reply_id: int, vote_data: VoteCreate, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)

    if not topics_service.get_by_id(topic_id):
        return BadRequest(f"Topic {topic_id} not found.")

    new_vote = votes_service.vote(reply_id=reply_id, user_id=user.id, type_vote=vote_data.type_vote)
    if not new_vote:
        return InternalServerError()

    return new_vote

@api_topics_router.post("/{topic_id}/best")
def choose_best_reply(topic_id: int, body: BestReplyRequest, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)

    topic = topics_service.get_by_id(topic_id)
    if topic is None:
        return NotFound(f"Topic {topic_id} not found.")

    if topic.user_id != user.id:
        return Unauthorized("Only the topic author can select the best reply.")

    reply = replies_service.get_by_id(body.reply_id)
    if reply is None or reply.topic_id != topic_id:
        return BadRequest(f"Reply {body.reply_id} does not belong to topic {topic_id}.")

    if not topics_service.select_best_reply(topic_id, body.reply_id):
        return BadRequest("Failed to set best reply; please try again.")

    return NoContent()

@api_topics_router.patch("/{id}/lock",response_model=Topic)
def set_topic_lock(id: int, topic_data: TopicLockRequest, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)
    if not user.is_admin:
        return Unauthorized("Admin access required.")

    topic = topics_service.get_by_id(id)
    if not topic:
        return NotFound(f"Topic {id} not found.")

    if not topics_service.set_locked(id, topic_data.is_locked):
        return BadRequest("Could not update topic lock status.")

    return topics_service.get_by_id(id)