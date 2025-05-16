from fastapi import APIRouter, Request, Form
from starlette.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

from common.template_config import CustomJinja2Templates
from data.models import TopicCreate
from services import topics_service, categories_service
from common import authenticate

topic_router = APIRouter(prefix='/topics')
templates = CustomJinja2Templates(directory='templates')

@topic_router.get("")
def view_topics(request: Request):
    user = authenticate.get_user_if_token(request)
    topics = list(topics_service.all())
    categories = list(categories_service.all())
    categories_dict = {c.id: c for c in categories}
    return templates.TemplateResponse(
        request=request,
        name="topics.html",
        context={
            "request": request,
            "user": user,
            "topics": topics,
            "categories": categories_dict
        }
    )

@topic_router.get("/create")
def create_topic_form(request: Request):
    user = authenticate.get_user_if_token(request)
    categories = list(categories_service.all())
    categories_dict = {cat.id: cat for cat in categories}
    return templates.TemplateResponse(
        request=request,
        name="create_topic.html",
        context={"request": request, "user": user, "categories": categories_dict}
    )

@topic_router.post("/create")
def create_topic(request: Request, title: str = Form(...),content: str = Form(...), category_id: int = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    topic_data = TopicCreate(title=title, content=content, category_id=category_id)
    topics_service.create(topic_data, user.id)

    return RedirectResponse(url="/topics", status_code=302)