from fastapi import FastAPI
from routers.users import router as users_router
from utils.console_messages import console_message_log
import uvicorn

app = FastAPI()

# Homepage
@app.get('/')
def homepage():
    return {"message": "Hello World!"}

app.include_router(users_router, prefix="/users", tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
    print(*console_message_log(), sep="\n")