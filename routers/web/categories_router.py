from fastapi import APIRouter, Request, Form
from starlette.responses import RedirectResponse

from common import authenticate
from common.template_config import CustomJinja2Templates
from data.models import TopicCreate
from services import categories_service, topics_service

category_router = APIRouter(prefix='/categories')
templates = CustomJinja2Templates(directory='templates')

@category_router.get("")
def get_categories(request: Request):
    user = authenticate.get_user_if_token(request)

    categories = list(categories_service.all())
    return templates.TemplateResponse(
        request=request,
        name="categories.html",
        context={"request": request, "user": user,"categories": categories}
    )

@category_router.get("/{id}")
def get_category_details(id: int, request: Request):
    user = authenticate.get_user_if_token(request)

    category = categories_service.get_by_id(id)
    if not category:
        return templates.TemplateResponse(
            request=request,
            name="not_found.html",
            context={"request": request, "user": user, "message": f"Category {id} not found."}
        )

    topics = list(categories_service.topics_by_category(category_id=id))
    categories = list(categories_service.all())
    categories_dict = {cat.id: cat for cat in categories}

    return templates.TemplateResponse(
        request=request,
        name="category_details.html",
        context={
            "request": request,
            "category": category,
            "topics": topics,
            "categories": categories_dict,
            "user": user
        }
    )

@category_router.post("/{id}/topics")
def create_topic_for_category(
    id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    topic_data = TopicCreate(title=title, content=content, category_id=id)
    topics_service.create(topic_data, user.id)

    return RedirectResponse(url=f"/categories/{id}", status_code=302)

