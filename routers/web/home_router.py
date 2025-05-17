from common.template_config import CustomJinja2Templates
import common.authenticate as authenticate
from fastapi import APIRouter, Request
from data.database import NASA_API_KEY
import traceback
import httpx

NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
home_router = APIRouter(prefix='')
templates = CustomJinja2Templates(directory='templates')

@home_router.get('/api/apod')
async def get_apod():
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(NASA_APOD_URL, params={"api_key": NASA_API_KEY})
            if resp.status_code == 200:
                return resp.json()
    except Exception:
        print(traceback.format_exc())
    return {"error": "NASA API unavailable"}

@home_router.get('/')
async def serve_index(request: Request):
    user = None
    token = request.cookies.get('u-token')
    if token:
        try:
            user = authenticate.get_user_or_raise_401(token)
        except Exception:
            user = None

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": user}
    )