from services.user_service import is_user_authenticated, find_user_by_token
from fastapi import HTTPException
from data.models import User

def get_user_or_raise_401(token: str) -> User:
    if not is_user_authenticated(token):
        raise HTTPException(status_code=401)

    return find_user_by_token(token)
