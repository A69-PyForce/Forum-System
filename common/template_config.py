from fastapi.templating import Jinja2Templates
from common.authenticate import get_user_if_token
from services.users_service import *

class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = get_user_if_token
        self.env.globals['get_avatar_by_username'] = get_avatar_by_username
        self.env.globals['get_avatar_by_user_id'] = get_avatar_by_user_id
        self.env.globals['find_user_by_id'] = find_user_by_id
        