from fastapi.templating import Jinja2Templates
from common.authenticate import get_user_if_token
from services.users_service import get_avatar_url

class CustomJinja2Templates(Jinja2Templates):
    def __init__(self, directory: str):
        super().__init__(directory=directory)
        self.env.globals['get_user'] = get_user_if_token
        self.env.globals['get_avatar_url'] = get_avatar_url