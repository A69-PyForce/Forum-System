from fastapi import APIRouter


topics_router = APIRouter(prefix="/topics")

@topics_router.get("/")
def get_topics(name: str, is_private: int, is_locked: int):
    pass