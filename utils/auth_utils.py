from jose import jwt, exceptions
from data.models import User
import hashlib
import json

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: Must have a encrypt_key.json file for user tokens:        #
# {                                                               #
#    "key": "secret_key"                                          #
# }                                                               #
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