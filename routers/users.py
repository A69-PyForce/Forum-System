from fastapi import APIRouter
import services.user_services

router = APIRouter()

@router.get('/')
def fetch_users(
    sort: str | None = None,
    search: str | None = None
):
    return {"message": "Not implemented"}