from fastapi import APIRouter
from common import responses
from data.models import Topic
from services import topics_service

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
    else:
        return topic
