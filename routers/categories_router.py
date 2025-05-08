from fastapi import APIRouter
from pydantic import BaseModel
from common.responses import NotFound
from data.models import TopicCreate, Category, Topic
from services import topics_service, categories_service



class CategoryTopicResponseModel(BaseModel):
    category: Category
    topics: list[Topic]

categories_router = APIRouter(prefix="/categories")


@categories_router.get('/')
def get_categories():
    """
    Retrieve all categories.

    Returns:
        Generator[Category]: A generator yielding Category instances for every row in the categories table.
    """
    return categories_service.all()

@categories_router.get("/{id}/topics")
def get_category_by_id(
        id: int,
        search: str | None = None,
        sort: str | None = None,
        sort_by: str | None = None,
        page: int = 1,
        size: int = 5):

    category = categories_service.get_by_id(id)
    if not category:
        return NotFound(f"Category with ID '{id}' not found.")

    offset = (page - 1) * size
    result = categories_service.topics_by_category(category_id=id, search=search, limit=size, offset=offset)
    topics = list(result)

    if sort in ("asc", "desc"):
        return topics_service.sort(topics, reverse=sort == 'desc', attribute=sort_by)

    return CategoryTopicResponseModel(category=category, topics=topics)

@categories_router.post("/")
def create_category(create_topic: TopicCreate, u_token: str = None):
    new_topic = categories_service.create(create_topic)
