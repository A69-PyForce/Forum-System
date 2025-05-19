from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from common.template_config import CustomJinja2Templates
from fastapi.responses import RedirectResponse
from data.models import Category, TopicCreate
from services import categories_service
from data.database import CLDNR_CONFIG
from services import topics_service
from common import authenticate
import cloudinary.uploader
from PIL import Image
import traceback
import io

category_router = APIRouter(prefix='/categories')
templates = CustomJinja2Templates(directory='templates')

@category_router.get("")
def get_categories(request: Request):
    """
    Render a page displaying all forum categories.

    Args:
        request (Request): The current HTTP request.

    Returns:
        TemplateResponse: The rendered template showing the list of categories.
    """
    user = authenticate.get_user_if_token(request)

    categories = list(categories_service.all())
    return templates.TemplateResponse(
        request=request,
        name="categories_list.html",
        context={"request": request, "user": user,"categories": categories}
    )

@category_router.get("/{id}")
def get_category_details(id: int, request: Request):
    """
    Render a page showing details for a specific category, including its topics.

    Args:
        id (int): The category ID.
        request (Request): The current HTTP request.

    Returns:
        TemplateResponse or RedirectResponse: The rendered details page, or a redirect if the category is not found.
    """
    user = authenticate.get_user_if_token(request)
    is_admin = user and user.is_admin

    category = categories_service.get_by_id(id)

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

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
    """
    Create a new forum category (admin only).

    Args:
        request (Request): The current HTTP request.
        name (str): The category name from the submitted form.

    Returns:
        RedirectResponse: Redirects to the categories list with a success or failure status.
    """
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="User must be logged in")
    
    try:
        category = Category(name=name, is_private=0, is_locked=0)
        categories_service.create(category)
        return RedirectResponse(url="/categories?created=1", status_code=302)
    except:
        print(traceback.format_exc())
        return RedirectResponse(url="/categories?created=0", status_code=302)  

@category_router.post("/{id}/topics")
def create_topic_for_category(
    id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(...)):
    """
    Create a new topic in a given category (user must be logged in).

    Args:
        id (int): The category ID.
        request (Request): The current HTTP request.
        title (str): The topic title from the form.
        content (str): The topic content from the form.

    Returns:
        RedirectResponse: Redirects to the category details page, or to login if not authenticated.
    """
    user = authenticate.get_user_if_token(request)
    if not user:
        raise HTTPException(status_code=403, detail="User must be logged in")

    try:
        topic_data = TopicCreate(title=title, content=content, category_id=id)
        topics_service.create(topic_data, user.id)
        return RedirectResponse(url=f"/categories/{id}", status_code=302)
    
    except:
        print(traceback.format_exc())
        category = categories_service.get_by_id(id)
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
            "user": user,
            "created": "0",
            "is_admin": user.is_admin,
            "error": "Category creation failed."
        })

    
@category_router.post("/{id}/toggle-lock")
def category_lock(id: int, request: Request):
    """
    Toggle the locked/unlocked status of a category (admin only).

    Args:
        id (int): The category ID.
        request (Request): The current HTTP request.

    Returns:
        RedirectResponse: Redirects to the category details page or home if unauthorized.
    """
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    category = categories_service.get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    categories_service.set_locked(id, not category.is_locked)
    return RedirectResponse(url=f"/categories/{id}", status_code=302)

@category_router.post("/{id}/toggle-private")
def toggle_category_privacy(id: int, request: Request):
    """
    Toggle the privacy (public/private) status of a category (admin only).

    Args:
        id (int): The category ID.
        request (Request): The current HTTP request.

    Returns:
        RedirectResponse: Redirects to the category details page or home if unauthorized.
    """
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")

    category = categories_service.get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    categories_service.set_privacy(id, not category.is_private)
    return RedirectResponse(url=f"/categories/{id}", status_code=302)

@category_router.post("/{id}/image")
async def upload_category_image(request: Request, id: int, file: UploadFile = File(...)):
    """
    Upload and set a new image for a category (admin only). Resizes image and uploads to Cloudinary if configured.

    Args:
        request (Request): The current HTTP request.
        id (int): The category ID.
        file (UploadFile): The uploaded image file.

    Returns:
        RedirectResponse or TemplateResponse: Redirects on success, or renders the details page with an error message on failure.
    """
    user = authenticate.get_user_if_token(request)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access only")
    
    if CLDNR_CONFIG:
        
        try:
            image_contents = await file.read()
            image = Image.open(io.BytesIO(image_contents))
            resized_image = image.resize((256, 128))
            buffer = io.BytesIO()
            resized_image.save(buffer, format=image.format or "JPEG")
            buffer.seek(0)
            result = cloudinary.uploader.upload(buffer, folder="forum-system-category-images")
            image_url = result["secure_url"]
            categories_service.update_category_image_url(id, image_url)
            return RedirectResponse(f"/categories/{id}", status_code=302)
        
        except:
            print(traceback.format_exc())
            category = categories_service.get_by_id(id)
            topics = list(categories_service.topics_by_category(id))
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
                    "is_admin": user.is_admin,
                    "user": user,
                    "error": "Image upload failed."
            })