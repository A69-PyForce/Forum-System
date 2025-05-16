from data.models import User, UserLoginData, UserRegisterData
from mariadb import IntegrityError
from utils.auth_utils import *

# Default db import, will be overriden when injected
import data.database as db

def _get_db(test_db = None):
    """
    Helper function that gets the database object to use for queries.

    Args:
        test_db: Optional database object for testing.

    Returns:
        Database object to use for queries.
    """
    return test_db or db

def register_user(user: UserRegisterData, test_db = None) -> User | None:
    """
    Register a new user in the database.

    Args:
        user (UserRegisterData): The user's registration data.
        test_db: Optional database object for testing.

    Returns:
        User: The created User object with generated ID if successful.
        None: If registration failed because of duplicate name key.
    """
    used_db = _get_db(test_db)
    
    hashed_password = hash_user_password(user.password)
    try:
        generated_id = used_db.insert_query(
            "INSERT INTO users(username, password_hash, is_admin) VALUES (?, ?, ?)",
            (user.username, hashed_password, user.is_admin,))
        return User(id=generated_id, username=user.username, password="", is_admin=user.is_admin,)
    except IntegrityError: return None
    
def login_user(login_data: UserLoginData, test_db = None) -> User | None:
    """
    Authenticate a user by username and password.

    Args:
        login_data (UserLoginData): The user's login credentials.
        test_db: Optional database object for testing.

    Returns:
        User: The authenticated User object if credentials are valid.
        None: If authentication fails.
    """
    used_db = _get_db(test_db)
    
    hashed_password = hash_user_password(login_data.password)
    query_data = used_db.read_query(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (login_data.username, hashed_password,))

    # if not query_data: return None
    return next((User.from_query_result(*row) for row in query_data), None)
    
def find_user_by_username(username: str, test_db = None) -> User | None:
    """
    Find a user by username.

    Args:
        username (str): The username to search for.
        test_db: Optional database object for testing.

    Returns:
        User: The User object if found.
        None: If not found.
    """
    used_db = _get_db(test_db)
    
    user_data = used_db.read_query("SELECT * FROM users WHERE username = ?", (username,))
    return next((User.from_query_result(*row) for row in user_data), None)
    
def find_user_by_id(id: int, test_db = None) -> User | None:
    """
    Find a user by ID.

    Args:
        id (int): The user ID to search for.
        test_db: Optional database object for testing.

    Returns:
        User: The User object if found.
        None: If not found.
    """
    used_db = _get_db(test_db)
    
    user_data = used_db.read_query("SELECT * FROM users WHERE id = ?", (id,))
    return next((User.from_query_result(*row) for row in user_data), None)

def find_user_by_token(token: str, test_db = None) -> User | None:
    """
    Decode a user token and return the corresponding User object.

    Args:
        token (str): The user authentication token.
        test_db: Optional database object for testing.

    Returns:
        User: The User object if found.
        None: If not found or token is invalid.
    """
    result = decode_user_token(token)
    if not result: return None
    _, username = result.values()
    return find_user_by_username(username, test_db)

def is_user_authenticated(token: str, test_db = None) -> bool:
    """
    Check if a user token is valid and corresponds to an existing user.

    Args:
        token (str): The user authentication token.
        test_db: Optional database object for testing.

    Returns:
        bool: True if the token is valid and user exists, False otherwise.
    """
    used_db = _get_db(test_db)
    
    decoded = decode_user_token(token)
    if not decoded: return False
    
    id, username = decoded.values()
    db_user = used_db.read_query("SELECT id, username FROM users WHERE id = ? AND username = ?", (id, username,))
    if not db_user: return False
    
    return True

def update_user_avatar_url(user_id: int, avatar_url: str, test_db = None) -> bool:
    """
    Update the avatar_url of a given user.
    
    Args:
        user_id (int): The id of the user.
        avatar_url (str): The new avatar url.
        test_db: Optional database object for testing.
        
    Returns:
        bool: True if update successful, False otherwise.
    """
    used_db = _get_db(test_db)
    return used_db.update_query("UPDATE users SET avatar_url = ? WHERE id = ?", (avatar_url, user_id,))

def get_avatar_url(username: str, test_db = None) -> str | None:
    """
    Get the avatar url of a given user.
    
    Args:
        username (str): The username of the user.
        test_db: Optional database object for testing.
        
    Returns:
        str: The avatar url,
        None: If avatar url is NULL in db.
    """
    used_db = _get_db(test_db)
    return used_db.read_query("SELECT avatar_url FROM users WHERE username = ?", (username,))[0][0]
    