from data.models import UserRegisterData, UserLoginData, User
import services.users_service as user_service
from common import responses, authenticate
from fastapi import APIRouter, Header

api_users_router = APIRouter(prefix='/api/users')

@api_users_router.post('/login')
def user_login(login_data: UserLoginData):
    """
    Authenticate a user and return a token if successful.

    Args:
        login_data (UserLoginData): The user's login credentials.

    Returns:
        str: User authentication token if login is successful.
        BadRequest: If login data is invalid.
        None: If login fails.
    """
    user = user_service.login_user(login_data)
    if not user:
        return responses.BadRequest('Invalid login data.')
    return user_service.encode_user_token(user)
    
    
@api_users_router.post('/register')
def user_register(user_data: UserRegisterData):
    """
    Register a new user.

    Args:
        user_data (UserRegisterData): The user's registration data.

    Returns:
        Created: If user is successfully registered.
        BadRequest: If username is already in use or registration data is invalid.
    """
    # Check if username exists
    if user_service.find_user_by_username(user_data.username):
        return responses.BadRequest(f"Username '{user_data.username}' is already in use.")
    user = user_service.register_user(user_data)
    if not user: responses.BadRequest('Invalid register data.')
    return responses.Created('User created.')

@api_users_router.get('/info', response_model=User, response_model_exclude={"password"})
def user_info(u_token: str = Header()):
    """
    Retrieve information about the authenticated user.

    Args:
        u_token (str): User authentication token from header.

    Returns:
        User: The authenticated user's information, excluding password.
    """
    return authenticate.get_user_or_raise_401(u_token)