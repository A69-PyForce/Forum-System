from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("static/images/favicon.ico")

# =============================== API ROUTERS ===============================
from routers.api.users_router import api_users_router
from routers.api.conversations_router import api_conversations_router
from routers.api.topics_router import api_topics_router
from routers.api.categories_router import api_categories_router
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
app.include_router(api_users_router, tags=["API - Users"])
app.include_router(api_conversations_router, tags=["API - Conversations"])
app.include_router(api_topics_router, tags=["API - Topics"])
app.include_router(api_categories_router, tags=["API - Categories"])
# ============================================================================

# =============================== WEB ROUTERS ===============================
from routers.web.home_router import home_router
from routers.web.users_router import users_router
from routers.web.conversations_router import conversations_router
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
app.include_router(home_router, tags=["WEB - Home"])
app.include_router(users_router, tags=["WEB - Users"])
app.include_router(conversations_router, tags=["WEB - Conversations"])
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)