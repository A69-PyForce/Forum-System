from fastapi import FastAPI
from routers.products import router as products_router

app = FastAPI()

# Homepage
@app.get('/')
def home():
    return {"msg": "Wooow such fancy homepage O_o"}

app.include_router(products_router, prefix="/products", tags=["Products"])