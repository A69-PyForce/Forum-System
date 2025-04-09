from fastapi import APIRouter
from services.products_service import get_products

router = APIRouter()

@router.get('/')
def fetch_products(
    sort: str | None = None,
    search: str | None = None
):
    return get_products(sort, search)