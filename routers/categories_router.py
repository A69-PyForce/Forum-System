from fastapi import APIRouter, Header
from pydantic import BaseModel
from common.authenticate import get_user_or_raise_401
from common.responses import NotFound, Unauthorized, BadRequest
from data.models import TopicCreate, Category, Topic, CategoryPrivacyUpdate
from services import topics_service, categories_service


class CategoryTopicResponseModel(BaseModel):
    category: Category
    topics: list[Topic]

class CategoryCreate(BaseModel):
    name: str

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
def create_category(category_data: CategoryCreate, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)
    if not user.is_admin:
        return Unauthorized("Admin access required.")

    name = category_data.name.strip()
    if not name:
        return BadRequest("Category name must not be empty.")

    new_category = categories_service.create(name)
    return new_category

@categories_router.patch("/{id}/privacy", response_model=Category)
def update_category_privacy(id: int, category_data: CategoryPrivacyUpdate, u_token: str = Header()):
    user = get_user_or_raise_401(u_token)
    if not user.is_admin:
        return Unauthorized("Admin access required.")

    category = categories_service.get_by_id(id)
    if not category:
        return NotFound(f"Category with ID '{id}' not found.")

    updated = categories_service.set_privacy(id, category_data.is_private)
    if not updated:
        return BadRequest("Could not update privacy. Try again?")
    return categories_service.get_by_id(id)
