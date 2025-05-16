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
    is_admin = user and user.is_admin

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

    created = request.query_params.get("created")

    return templates.TemplateResponse(
        request=request,
        name="category_details.html",
        context={
            "request": request,
            "category": category,
            "topics": topics,
            "categories": categories_dict,
            "user": user,
            "created": created == "1",
            "is_admin": is_admin
        }
    )

@category_router.post("/create")
def create_category(request: Request, name: str = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        return RedirectResponse(url="/login", status_code=302)

    categories_service.create(name)
    return RedirectResponse(url="/categories?created=1", status_code=302)

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

@category_router.post("/{id}/toggle-lock")
def category_lock(id: int, request: Request):
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)

    category = categories_service.get_by_id(id)
    if not category:
        return RedirectResponse(url="/categories", status_code=302)

    categories_service.set_locked(id, not category.is_locked)
    return RedirectResponse(url=f"/categories/{id}", status_code=302)

@category_router.post("/{id}/toggle-private")
def toggle_category_privacy(id: int, request: Request):
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        return RedirectResponse(url="/", status_code=302)

    category = categories_service.get_by_id(id)
    if not category:
        return RedirectResponse(url="/categories", status_code=302)

    categories_service.set_privacy(id, not category.is_private)
    return RedirectResponse(url=f"/categories/{id}", status_code=302)