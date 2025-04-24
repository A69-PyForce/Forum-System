from fastapi import APIRouter
from data.models import TopicCreate

topics_router = APIRouter(prefix="/topics")

@topics_router.get("/")
def get_topics():
    pass

@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    pass

@topics_router.post('/')
def create_topic(topic: TopicCreate):
    pass