from services.users_service import is_user_authenticated, find_user_by_token
from fastapi import HTTPException, Request
from data.models import User

def get_user_or_raise_401(u_token: str) -> User:
    """Get User obj from u_token string or raise 401 Unauthorized."""
    if not is_user_authenticated(u_token):
        raise HTTPException(status_code=401, detail="Invalid u-token.")

    return find_user_by_token(u_token)

def get_user_if_token(request: Request) -> User | None:
    """Get User obj from Request cookies or None."""
    token = request.cookies.get('token')
    return find_user_by_token(token)