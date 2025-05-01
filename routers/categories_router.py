from fastapi import APIRouter
from services.categories_service import all as get_all_categories


categories_router = APIRouter(prefix="/categories")


@categories_router.get("/")
def get_categories():
    return list(get_all_categories())