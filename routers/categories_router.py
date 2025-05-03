from fastapi import APIRouter
from data.models import TopicCreate
from services import topics_service, categories_service
from services.categories_service import topics_by_category


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
    """
    Retrieve topics belonging to a specific category, with optional filtering, sorting, and pagination.

    Args:
        id (int): The ID of the category to fetch topics for.
        search (str | None): Optional substring to filter topics by title.
        sort (str | None): Sort order; must be 'asc' or 'desc' to apply sorting.
        sort_by (str | None): Attribute name to sort by (e.g., 'title', 'content').
        page (int): Page number for pagination (1-indexed).
        size (int): Number of items per page.

    Returns:
        list[Topic]: A list of Topic instances matching the query parameters.
    """
    offset = (page - 1) * size
    result = topics_by_category(id, search, limit=size, offset=offset)

    if sort in ("asc", "desc"):
        return topics_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result

@categories_router.post("/")
def create_category(create_topic: TopicCreate, u_token: str = None):
    new_topic = categories_service.create(create_topic)
