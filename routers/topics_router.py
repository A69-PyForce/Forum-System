from fastapi import APIRouter, Header
from pydantic import BaseModel
from common import responses
from common.authenticate import get_user_or_raise_401
from data.models import Topic, Reply, TopicCreate
from services import topics_service, replies_service, categories_service


class TopicResponseModel(BaseModel):
    topic: Topic
    replies: list[Reply]

topics_router = APIRouter(prefix="/topics")

@topics_router.get("/",response_model=list[Topic])
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None,
    page: int = 1,
    size: int = 5
):
    offset = (page - 1) * size

    result = topics_service.all(search, limit=size, offset=offset)

    if sort and (sort == "asc" or sort == "desc"):
        return topics_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result


@topics_router.get("/{id}")
def get_topic_by_id(id: int):
    topic = topics_service.get_by_id(id)

    if topic is None:
        return responses.NotFound(f"Topic with ID '{id}' not found.")

    replies = list(replies_service.get_by_topic(topic.id))

    return TopicResponseModel(topic=topic,replies=replies)

@topics_router.post("/", status_code=201)
def create_topic(topic: TopicCreate, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)

    if not categories_service.exists(topic.categories_id):
        return responses.BadRequest("Category does not exist.")

    new_topic = topics_service.create(topic, user.id)
    if not new_topic:
        return responses.BadRequest("Failed to create topic. Please check your payload.")

    return new_topic
