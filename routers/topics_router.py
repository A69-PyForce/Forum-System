from fastapi import APIRouter
from services import topics_service

topics_router = APIRouter(prefix="/topics")

@topics_router.get("/")
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None
):
    result = topics_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topics_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result
