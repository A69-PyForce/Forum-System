from jose import jwt, exceptions
from dotenv import load_dotenv
from data.models import User
import hashlib
import os

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a .env file for auth utils.                     #
#       Check README for instructions.                            #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Load environment variables from .env file
load_dotenv()
_ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")

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