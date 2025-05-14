from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

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
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
app.include_router(home_router, tags=["WEB - Home"])
app.include_router(users_router, tags=["WEB - Users"])
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)