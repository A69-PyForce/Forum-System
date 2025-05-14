import unittest
from users_service_test import fake_user
import utils.auth_utils as auth_utils


_INVALID_TOKEN = "I am an invalid token :)"
_INVALID_USER = "I am an invalid user :)"
_UNIQUE_PASSWORDS = (
    'f1GIaIUfpdxKhDGM', '8Lww5wKjJSLfNwtTExO40', 
    'Qsu1Ule5k8MZDRBnPotdi', 'GfEe5avC', 
    'o6zDaTrcErQLQtqj7', 'BJtqubaWwogmxUpgVvBxZXPGD1', 
    'Y7pHXM1wRtCYmE77ok2qp', 'VAjTivErZgh4u7VAa22bGzX', 
    'M7YAKvO4Ph8B97iVbMOgun7RLGfM2H', '6cTRlMXqEduWe1jVG1'
)

class AuthUtilsTest(unittest.TestCase):
    def test_generate_userToken_returns_correctInstance(self):
        user = fake_user()
        
        result = auth_utils.encode_user_token(user)
        self.assertIsInstance(result, str)
        
    def test_generate_userToken_returns_noneType_when_invalidParams(self):
        result = auth_utils.encode_user_token(_INVALID_USER)
        self.assertIsNone(result)
        
    def test_decode_userToken_returns_correctDict(self):
        user = fake_user()
        
        token = auth_utils.encode_user_token(user)
        result = auth_utils.decode_user_token(token)
        self.assertEqual(result["id"] == user.id, result["username"] == user.username)
        
    def test_decode_userToken_returns_noneType_when_invalidParams(self):
        result = auth_utils.decode_user_token(_INVALID_TOKEN)
        self.assertIsNone(result)
        
    def test_hash_userPassword_returns_correctResult(self):
        user = fake_user()
        
        result = auth_utils.hash_user_password(user.password)
        self.assertIsInstance(result, str)
        # sha224 algorithm always returns string with 56 characters
        self.assertEqual(len(result), 56)
        
    def test_hash_userPassword_alwaysReturns_sameHash_for_samePassword(self):
        user = fake_user()
        set_hashes = set() # If len of set > 1 => hashing returns different values
        
        for _ in range(10): set_hashes.add(auth_utils.hash_user_password(user.password))
        self.assertEqual(len(set_hashes), 1)
        
    def test_hash_userPassword_returns_differentHash_for_differentPasswords(self):
        set_hashes = set() # If len of set < 10 => hashing returns same values
        
        for i in range(len(_UNIQUE_PASSWORDS)): set_hashes.add(auth_utils.hash_user_password(_UNIQUE_PASSWORDS[i]))
        self.assertEqual(len(set_hashes), 10)