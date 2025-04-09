from fastapi import FastAPI
from db import *

app = FastAPI()

@app.get('/')
def home():
    return {"msg": "Wooow such fancy homepage O_o"}

@app.get('/products')
def get_products(
    sort: str | None = None,
    search: str | None = None
):
    products = fetch_products(search=search, sort=sort)
    return products