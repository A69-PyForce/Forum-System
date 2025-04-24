import sys
from pathlib import Path

# Add the parent directory of main-repo to the Python path
# Allows imports from other folders
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.database import read_query, insert_query
from data.models import User, UserLoginData
from jose import jwt
import hashlib
import json

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a encrypt_key.json file for user tokens.        #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Read encryption key from file
with open ('encrypt_key.json', 'r') as file:
    _ENCRYPT_KEY = json.load(file)["key"]

def generate_user_token(user: User) -> str:
    """Generates a token from the User object. Returns the token string."""
    
    return jwt.encode({"id": user.id, "username": user.username}, _ENCRYPT_KEY, algorithm='HS256')

def decode_user_token(token: str) -> dict:
    """Decodes a user token using the encryption key. Returns dict: {"id": int, "username": str}."""
    
    return jwt.decode(token, _ENCRYPT_KEY, algorithms=['HS256'])

def hash_user_password(password: str) -> str:
    """Irreversibly hashes a password from a password string. Returns the generated string."""
    
    return hashlib.sha224(password.encode('utf-8')).hexdigest()

def login_user(login_data: UserLoginData) -> User | None:
    """Tries to find a user from the database. Returns a User object if found or None if not."""
    
    hashed_password = hash_user_password(login_data.password)
    query_data = read_query(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (login_data.username, hashed_password,))

    if not query_data: return None
    return next((User.from_query_result(*row) for row in query_data), None)

def register_user(user: User) -> User | None:
    """Register a User into the database. If successful, returns the User object \n 
    with the generated id from DB, or None if some issue occured during execution."""
    
    hashed_password = hash_user_password(user.password)
    generated_id = insert_query(
        "INSERT INTO users(username, password_hash, is_admin) VALUES (?, ?, ?)",
        (user.username, hashed_password, user.is_admin,))
        
    if not generated_id: return None
        
    user.id = generated_id
    return user
    
def find_user_by_username(username: str) -> User | None:
    """Return a User object if username is found in database. Otherwise return None."""
    
    user_data = read_query("SELECT * FROM users WHERE username = ?", (username,))
    return next((User.from_query_result(*row) for row in user_data), None)
    
def find_user_by_id(id: int) -> User | None:
    """Return a User object if id is found in database. Otherwise return None."""
    
    user_data = read_query("SELECT * FROM users WHERE id = ?", (id,))
    return next((User.from_query_result(*row) for row in user_data), None)

def is_user_authenticated(token: str) -> bool:
    """Decode a user token, generated with the generate_user_token function. \n
    Returns True if token is valid, False otherwise."""
    
    id, username = decode_user_token(token).values()
    db_user = read_query("SELECT id, username FROM users WHERE id = ? AND username = ?", (id, username,))
    if db_user: return True
    return False

def find_user_by_token(token: str) -> User | None:
    """Decode a user token and return User object if found in database. Otherwise return None."""
    
    _, username = decode_user_token(token).values()
    return find_user_by_username(username)
    

if __name__ == "__main__": # test some functions if file is run as main
    user = User(id=1, username='emko', password='123', is_admin=1)
    token = generate_user_token(user)
    print("user token:", token)
    print("decoded user token:", decode_user_token(token))
    print("hashed user password: ", hash_user_password(user))