from db import fetch_products_from_db

def get_products(sort: str | None, search: str | None):
    products = fetch_products_from_db(search, sort)
    return products