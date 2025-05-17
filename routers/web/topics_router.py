from fastapi import APIRouter, Request, Form
from starlette.responses import RedirectResponse
from common.template_config import CustomJinja2Templates
from data.models import TopicCreate, ReplyCreate
from services import topics_service, categories_service, replies_service, votes_service
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
        name="topics_list.html",
        context={
            "request": request,
            "user": user,
            "topics": topics,
            "categories": categories_dict
        }
    )

@topic_router.post("/{id}/replies")
def add_reply(id: int, request: Request, content: str = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse(url="/users/login", status_code=302)

    reply_data = ReplyCreate(text=content)
    replies_service.create(reply_data, user.id, id)

    return RedirectResponse(url=f"/topics/{id}", status_code=302)

@topic_router.get("/create")
def create_topic_form(request: Request):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)

    categories = list(categories_service.all())
    # categories_dict = {cat.id: cat for cat in categories}
    return templates.TemplateResponse(
        request=request,
        name="create_topic.html",
        context={"request": request, "user": user, "categories": categories}
    )

@topic_router.get("/{id}")
def topic_details(id: int, request: Request):
    user = authenticate.get_user_if_token(request)
    topic = topics_service.get_by_id(id)

    votes = votes_service.count_votes_for_replies(id)

    if not topic:
        return RedirectResponse(url="/topics", status_code=302)

    replies = sorted(replies_service.get_by_topic(topic.id), key=lambda r: (r.id != topic.best_reply_id, r.created_at))

    is_admin = user and user.is_admin

    return templates.TemplateResponse("topic_details.html", {
        "request": request,
        "user": user,
        "topic": topic,
        "replies": replies,
        "is_admin": is_admin,
        "votes": votes
    })

@topic_router.post("/create")
def create_topic(request: Request, title: str = Form(...),content: str = Form(...), category_id: int = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse(url="/users/login", status_code=302)

    topic_data = TopicCreate(title=title, content=content, category_id=category_id)
    topics_service.create(topic_data, user.id)

    return RedirectResponse(url="/topics", status_code=302)

@topic_router.post("/{topic_id}/best-reply/{reply_id}")
def mark_best_reply(topic_id: int, reply_id: int, request: Request):
    user = authenticate.get_user_if_token(request)
    topic = topics_service.get_by_id(topic_id)

    if not user or not topic or topic.user_id != user.id:
        return RedirectResponse(url=f"/topics/{topic_id}", status_code=302)

    topics_service.select_best_reply(topic_id, reply_id)

    return RedirectResponse(url=f"/topics/{topic_id}", status_code=302)

@topic_router.post("/{topic_id}/vote/{reply_id}")
def vote_reply(topic_id: int, reply_id: int, request: Request, type_vote: str = Form(...)):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)

    votes_service.vote(reply_id=reply_id, user_id=user.id, type_vote=type_vote)
    return RedirectResponse(f"/topics/{topic_id}", status_code=302)


@topic_router.post("/{id}/toggle-lock")
def toggle_lock(id: int, request: Request):
    user = authenticate.get_user_if_token(request)
    if not user:
        return RedirectResponse("/users/login", status_code=302)
    
    topic = topics_service.get_by_id(id)
    
    if user.id == topic.user_id or user.is_admin:
        topics_service.toggle_lock(id)
    
    return RedirectResponse(f"/topics/{id}", status_code=302)
