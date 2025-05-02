from fastapi import APIRouter
import common.responses
from data.models import Category
from services import topics_service
from services.categories_service import all as get_all_categories, topics_by_category

categories_router = APIRouter(prefix="/categories")


@categories_router.get("/", response_model=list[Category])
def get_categories():
    return list(get_all_categories())

@categories_router.get("/{id}/topics")
def get_category_by_id(
        id: int,
        search: str | None = None,
        sort: str | None = None,
        sort_by: str | None = None,
        page: int = 1,
        size: int = 5):

    offset = (page - 1) * size
    result = topics_by_category(id, search, limit=size, offset=offset)

    if sort in ("asc", "desc"):
        return topics_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result