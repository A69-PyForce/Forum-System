from fastapi import FastAPI

from routers.topics_router import topics_router
from routers.users_router import user_router
from routers.conversations_router import conversation_router
import uvicorn

app = FastAPI()

# Homepage
@app.get('/')
def homepage():
    return {"message": "Hello World!"}

app.include_router(user_router, tags=["Users"])
app.include_router(conversation_router, tags=["Conversations"])
app.include_router(topics_router, tags=["Topics"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)