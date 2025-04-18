from fastapi import FastAPI
from routers.users import user_router
from utils.console_messages import console_message_log
import uvicorn

app = FastAPI()

# Homepage
@app.get('/')
def homepage():
    return {"message": "Hello World!"}

app.include_router(user_router, tags=["Users"])

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
    print("~" * 50, "Console messages log", "~" * 50)
    print(*console_message_log(), sep="\n")