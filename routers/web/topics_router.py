from services import topics_service, categories_service, replies_service, votes_service
from fastapi import APIRouter, Request, Form, HTTPException
from common.template_config import CustomJinja2Templates
from starlette.responses import RedirectResponse
from data.models import TopicCreate, ReplyCreate
from common import authenticate
import traceback

topic_router = APIRouter(prefix='/topics')
templates = CustomJinja2Templates(directory='templates')

@topic_router.get("")
def view_topics(request: Request):
    """
    Render a page displaying all topics.

    Args:
        request (Request): The current HTTP request.

    Returns:
        TemplateResponse: The rendered template with a list of topics.
    """
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
    """
    Add a reply to a topic. User must be logged in.

    Args:
        id (int): The topic ID.
        request (Request): The current HTTP request.
        content (str): The reply content, from the form.

    Returns:
        RedirectResponse or TemplateResponse: Redirect to the topic, or re-render the topic page with an error.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")

    try:
        reply_data = ReplyCreate(text=content)
        replies_service.create(reply_data, user.id, id)
        return RedirectResponse(url=f"/topics/{id}", status_code=302) # refresh page
    except:
        print(traceback.format_exc())
        topic = topics_service.get_by_id(id)
        if not topic:
            raise HTTPException(status_code=404, detail="Topic not found")
        
        # place marked reply on top of all others
        replies = sorted(replies_service.get_by_topic(topic.id), key=lambda r: (r.id != topic.best_reply_id, r.created_at))
        votes = votes_service.count_votes_for_replies(id)
        is_admin = user and user.is_admin
        
        return templates.TemplateResponse(request=request, name="topic_details.html", context={
        "request": request, "user": user, "topic": topic, "replies": replies, "is_admin": is_admin, "votes": votes,
        "error": "An error occured while creating your reply."})

@topic_router.get("/create")
def create_topic_form(request: Request):
    """
    Render the form for creating a new topic.

    Args:
        request (Request): The current HTTP request.

    Returns:
        TemplateResponse or RedirectResponse: The topic creation form, or redirect to login if not authenticated.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")

    categories = list(categories_service.all())
    return templates.TemplateResponse(
        request=request,
        name="create_topic.html",
        context={"request": request, "user": user, "categories": categories
    })

@topic_router.get("/{id}")
def topic_details(id: int, request: Request):
    """
    Render a page displaying the details of a single topic, including replies.

    Args:
        id (int): The topic ID.
        request (Request): The current HTTP request.

    Returns:
        TemplateResponse or RedirectResponse: The topic details template, or redirect to topics list if not found.
    """
    user = authenticate.get_user_if_token(request)
    
    topic = topics_service.get_by_id(id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    votes = votes_service.count_votes_for_replies(id)
    # place marked reply on top of all others
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
    """
    Handle submission of the new topic creation form.

    Args:
        request (Request): The current HTTP request.
        title (str): The topic title.
        content (str): The topic content.
        category_id (int): The category ID for the new topic.

    Returns:
        RedirectResponse or TemplateResponse: Redirect to topics list on success, or re-render the form with an error.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")

    try:
        topic_data = TopicCreate(title=title, content=content, category_id=category_id)
        topics_service.create(topic_data, user.id)
        return RedirectResponse(url="/topics", status_code=302) # refresh page
    except:
        print(traceback.format_exc())
        categories = list(categories_service.all())
        return templates.TemplateResponse(request=request, name="create_topic.html", context={
            "request": request, "user": user, "categories": categories, "error": "An issue occured while creating your topic."
        })

@topic_router.post("/{topic_id}/best-reply/{reply_id}")
def mark_best_reply(topic_id: int, reply_id: int, request: Request):
    """
    Mark a reply as the best answer for a topic. Only the topic author can perform this.

    Args:
        topic_id (int): The topic ID.
        reply_id (int): The reply ID.
        request (Request): The current HTTP request.

    Returns:
        RedirectResponse: Redirects back to the topic details page.
    """
    user = authenticate.get_user_if_token(request)
    topic = topics_service.get_by_id(topic_id)

    if not user or not topic or topic.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized user")

    topics_service.select_best_reply(topic_id, reply_id)

    return RedirectResponse(url=f"/topics/{topic_id}", status_code=302)

@topic_router.post("/{topic_id}/vote/{reply_id}")
def vote_reply(topic_id: int, reply_id: int, request: Request, type_vote: str = Form(...)):
    """
    Upvote or downvote a reply for a topic.

    Args:
        topic_id (int): The topic ID.
        reply_id (int): The reply ID to vote on.
        request (Request): The current HTTP request.
        type_vote (str): The type of vote ('upvote' or 'downvote').

    Returns:
        RedirectResponse: Redirects back to the topic details page.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")

    votes_service.vote(reply_id=reply_id, user_id=user.id, type_vote=type_vote)
    return RedirectResponse(f"/topics/{topic_id}", status_code=302)


@topic_router.post("/{id}/toggle-lock")
def toggle_lock(id: int, request: Request):
    """
    Toggle the lock status of a topic (only for the topic author or admin).

    Args:
        id (int): The topic ID.
        request (Request): The current HTTP request.

    Returns:
        RedirectResponse: Redirects back to the topic details page.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")
    
    topic = topics_service.get_by_id(id)
    
    if user.id == topic.user_id or user.is_admin:
        topics_service.toggle_lock(id)
    
    return RedirectResponse(f"/topics/{id}", status_code=302)
