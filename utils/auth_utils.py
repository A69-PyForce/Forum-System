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

def encode_user_token(user: User) -> str | None:
    """
    Encode a JWT User token from a User object.

    Args:
        user (User): The user object to encode.

    Returns:
        str: The generated JWT token as a string if successful.
        None: If the input is not a valid User object.
    """
    if not isinstance(user, User): return None
    return jwt.encode({"id": user.id, "username": user.username}, _ENCRYPT_KEY, algorithm='HS256')

def decode_user_token(token: str) -> dict | None:
    """
    Decode a JWT User token using the encryption key.

    Args:
        token (str): The JWT token string.

    Returns:
        dict: A dictionary with user data ({"id": int, "username": str}) if decoding is successful.
        None: If decoding fails or the token is invalid.
    """
    try: return jwt.decode(token, _ENCRYPT_KEY, algorithms=['HS256'])
    except: return None 

def hash_user_password(password: str) -> str:
    """
    Irreversibly hash a password string using the SHA-224 algorithm.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password as a hexadecimal string.
    """
    return hashlib.sha224(password.encode('utf-8')).hexdigest()