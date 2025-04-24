from fastapi import APIRouter, Header
from common import responses, authenticate
from data.models import User, UserLoginData
import services.users_service as user_service

user_router = APIRouter(prefix='/users')

@user_router.post('/login')
def user_login(login_data: UserLoginData):
    user = user_service.login_user(login_data)
    
    if user:
        token = user_service.generate_user_token(user)
        return {"token": token}
    else:
        return responses.BadRequest('Invalid login data.')
    
@user_router.post('/register')
def user_register(user_data: User):
    user = user_service.register_user(user_data)
    if user: return user
    else: return responses.BadRequest('Invalid register data.')

@user_router.get('/info', response_model=User, response_model_exclude={"password"})
def user_info(u_token: str = Header()):
    return authenticate.get_user_or_raise_401(u_token)