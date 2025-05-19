from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import RequestValidationError
from common.template_config import CustomJinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request, FastAPI
from starlette.status import *
import uvicorn

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ API ROUTER IMPORTS ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from routers.api.users_router import api_users_router
from routers.api.conversations_router import api_conversations_router
from routers.api.topics_router import api_topics_router
from routers.api.categories_router import api_categories_router

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ WEB ROUTER IMPORTS ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from routers.web.home_router import home_router
from routers.web.users_router import users_router
from routers.web.conversations_router import conversations_router
from routers.web.topics_router import topic_router
from routers.web.categories_router import category_router


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ APP AND TEMPLATES ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
app = FastAPI()
templates = CustomJinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ EXCEPTION HANDLING ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
from fastapi.responses import JSONResponse

def is_api_request(request: Request) -> bool:
    return request.url.path.startswith("/api")

@app.exception_handler(404)
async def not_found(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Page Not Found"}, status_code=404)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 404, "message": "Page Not Found"}, status_code=404)

@app.exception_handler(400)
async def bad_request(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Bad Request"}, status_code=400)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 400, "message": "Bad Request"}, status_code=400)

@app.exception_handler(401)
async def unauthorized(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 401, "message": "Unauthorized"}, status_code=401)

@app.exception_handler(403)
async def forbidden(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Forbidden"}, status_code=403)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 403, "message": "Forbidden"}, status_code=403)

@app.exception_handler(405)
async def method_not_allowed(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Method Not Allowed"}, status_code=405)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 405, "message": "Method Not Allowed"}, status_code=405)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if is_api_request(request):
        return JSONResponse({"detail": "Unprocessable Content"}, status_code=422)
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": 422,
            "message": "Unprocessable Content"
        }, status_code=422)

@app.exception_handler(500)
async def internal_server_error(request: Request, exc: StarletteHTTPException):
    if is_api_request(request):
        return JSONResponse({"detail": "Internal Server Error"}, status_code=500)
    return templates.TemplateResponse("error.html", {"request": request, "status_code": 500, "message": "Internal Server Error"}, status_code=500)


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ GET ICON ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.ico")


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ API ROUTERS ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
app.include_router(api_users_router, tags=["API - Users"])
app.include_router(api_conversations_router, tags=["API - Conversations"])
app.include_router(api_topics_router, tags=["API - Topics"])
app.include_router(api_categories_router, tags=["API - Categories"])


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ WEB ROUTERS ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 
app.include_router(home_router, tags=["WEB - Home"])
app.include_router(users_router, tags=["WEB - Users"])
app.include_router(conversations_router, tags=["WEB - Conversations"])
app.include_router(topic_router, tags=["WEB - Topics"])
app.include_router(category_router, tags=["WEB - Categories"])


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ RUN SERVER ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
if __name__ == "__main__":  
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)