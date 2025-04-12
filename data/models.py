from pydantic import BaseModel

class User(BaseModel):
    """
    Model User, corresponding to the Database.
    """
    id: int | None = None
    username: str
    password: str
    is_admin: bool