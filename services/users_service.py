import sys
from pathlib import Path

# Add the parent directory of main-repo to the Python path
# Allows imports from other folders
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.models import User, UserLoginData, UserRegisterData

# Default db import, will be overriden when injected
import data.database as db

from jose import jwt, exceptions
import hashlib
import json

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a encrypt_key.json file for user tokens.        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Read encryption key from file
with open ('encrypt_key.json', 'r') as file:
    _ENCRYPT_KEY = json.load(file)["key"]

def generate_user_token(user: User) -> str | None:
    """Generates a token from the User object. Returns the token string or None if unsuccessful."""
    
    if not isinstance(user, User): return None
    return jwt.encode({"id": user.id, "username": user.username}, _ENCRYPT_KEY, algorithm='HS256')

def decode_user_token(token: str) -> dict | None:
    """Decodes a user token using the encryption key. Returns dict: {"id": int, "username": str} or None if unsuccessful."""
    
    try: return jwt.decode(token, _ENCRYPT_KEY, algorithms=['HS256'])
    except exceptions.JWTError: return None 

def hash_user_password(password: str) -> str:
    """Irreversibly hashes a password from a password string. Returns the generated string."""
    
    return hashlib.sha224(password.encode('utf-8')).hexdigest()

def register_user(user: UserRegisterData, test_db = None) -> User | None:
    """Register a User into the database. If successful, returns the User object \n 
    with the generated id from DB, or None if some issue occured during execution."""
    
    # DB Injection: default db from imports or test_db if param is != None.
    used_db = test_db or db
    
    hashed_password = hash_user_password(user.password)
    generated_id = used_db.insert_query(
        "INSERT INTO users(username, password_hash, is_admin) VALUES (?, ?, ?)",
        (user.username, hashed_password, user.is_admin,))
        
    if not generated_id: return None
    return User(id=generated_id, username=user.username, password="", is_admin=user.is_admin)

def login_user(login_data: UserLoginData, test_db = None) -> User | None:
    """Tries to find a user from the database. Returns a User object if found or None if not."""
    
    # DB Injection: default db from imports or test_db if param is != None.
    used_db = test_db or db
    
    hashed_password = hash_user_password(login_data.password)
    query_data = used_db.read_query(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (login_data.username, hashed_password,))

    # if not query_data: return None
    return next((User.from_query_result(*row) for row in query_data), None)
    
def find_user_by_username(username: str, test_db = None) -> User | None:
    """Return a User object if username is found in database. Otherwise return None."""
    
    # DB Injection: default db from imports or test_db if param is != None.
    used_db = test_db or db
    
    user_data = used_db.read_query("SELECT * FROM users WHERE username = ?", (username,))
    return next((User.from_query_result(*row) for row in user_data), None)
    
def find_user_by_id(id: int, test_db = None) -> User | None:
    """Return a User object if id is found in database. Otherwise return None."""
    
    # DB Injection: default db from imports or test_db if param is != None.
    used_db = test_db or db
    
    user_data = used_db.read_query("SELECT * FROM users WHERE id = ?", (id,))
    return next((User.from_query_result(*row) for row in user_data), None)

def find_user_by_token(token: str, test_db = None) -> User | None:
    """Decode a user token and return User object if found in database. Otherwise return None."""
    
    _, username = decode_user_token(token).values()
    return find_user_by_username(username, test_db)

def is_user_authenticated(token: str, test_db = None) -> bool:
    """Decode a user token, generated with the generate_user_token function. \n
    Returns True if token is valid, False otherwise."""
    
    # DB Injection: default db from imports or test_db if param is != None.
    used_db = test_db or db
    
    decoded = decode_user_token(token)
    if not decoded: return False
    
    id, username = decoded.values()
    db_user = used_db.read_query("SELECT id, username FROM users WHERE id = ? AND username = ?", (id, username,))
    if not db_user: return False
    
    return True