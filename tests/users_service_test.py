import unittest
from unittest.mock import Mock
from services import users_service
from data.models import User, UserLoginData, UserRegisterData
from data import database


_INVALID_TOKEN = "I am an invalid token :)"
_INVALID_USER = "I am an invalid user :)"
_UNIQUE_PASSWORDS = (
    'f1GIaIUfpdxKhDGM', '8Lww5wKjJSLfNwtTExO40', 
    'Qsu1Ule5k8MZDRBnPotdi', 'GfEe5avC', 
    'o6zDaTrcErQLQtqj7', 'BJtqubaWwogmxUpgVvBxZXPGD1', 
    'Y7pHXM1wRtCYmE77ok2qp', 'VAjTivErZgh4u7VAa22bGzX', 
    'M7YAKvO4Ph8B97iVbMOgun7RLGfM2H', '6cTRlMXqEduWe1jVG1'
)

def fake_user(id: int = 1, username: str = "emko", password: str = "Pass123!", is_admin: int = 1):
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.username = username
    mock_user.password = password
    mock_user.is_admin = is_admin
    return mock_user

class UsersServiceTest(unittest.TestCase):
        
    def test_generate_userToken_returns_correctInstance(self):
        user = fake_user()
        
        result = users_service.generate_user_token(user)
        self.assertIsInstance(result, str)
        
    def test_generate_userToken_returns_noneType_when_invalidParams(self):
        result = users_service.generate_user_token(_INVALID_USER)
        self.assertIsNone(result)
        
    def test_decode_userToken_returns_correctDict(self):
        user = fake_user()
        
        token = users_service.generate_user_token(user)
        result = users_service.decode_user_token(token)
        self.assertEqual(result["id"] == user.id, result["username"] == user.username)
        
    def test_decode_userToken_returns_noneType_when_invalidParams(self):
        result = users_service.decode_user_token(_INVALID_TOKEN)
        self.assertIsNone(result)
        
    def test_hash_userPassword_returns_correctResult(self):
        user = fake_user()
        
        result = users_service.hash_user_password(user.password)
        self.assertIsInstance(result, str)
        # sha224 algorithm always returns string with 56 characters
        self.assertEqual(len(result), 56)
        
    def test_hash_userPassword_alwaysReturns_sameHash_for_samePassword(self):
        user = fake_user()
        set_hashes = set() # If len of set > 1 => hashing returns different values
        
        for _ in range(10): set_hashes.add(users_service.hash_user_password(user.password))
        self.assertEqual(len(set_hashes), 1)
        
    def test_hash_userPassword_returns_differentHash_for_differentPasswords(self):
        set_hashes = set() # If len of set < 10 => hashing returns same values
        
        for i in range(len(_UNIQUE_PASSWORDS)): set_hashes.add(users_service.hash_user_password(_UNIQUE_PASSWORDS[i]))
        self.assertEqual(len(set_hashes), 10)
        
    def test_registerUser_returnsUser_when_usernameNotTaken(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.insert_query.return_value = 1
        
        register_data = UserRegisterData(username=user.username, password=user.password, is_admin=user.is_admin)
        result = users_service.register_user(register_data, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)
        
    def test_registerUser_returnsNone_when_usernameTaken(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.insert_query.return_value = 0
        
        register_data = UserRegisterData(username=user.username, password=user.password, is_admin=user.is_admin)
        result = users_service.register_user(register_data, mock_db)
        self.assertIsNone(result)
        
    def test_loginUser_returnsUser_when_userFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        login_data = UserLoginData(username=user.username, password=user.password)
        result = users_service.login_user(login_data, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, login_data.username)
        
    def test_loginUser_returnsNone_when_userNotFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        login_data = UserLoginData(username=user.username, password=user.password)
        result = users_service.login_user(login_data, mock_db)
        self.assertIsNone(result)
    
    def test_findUser_byUsername_returnsUser_when_userFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        result = users_service.find_user_by_username(user.username, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)
        
    def test_findUser_byUsername_returnsNone_when_userNotFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.find_user_by_username(user.username, mock_db)
        self.assertIsNone(result)
        
    def test_findUser_byId_returnsUser_when_userFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        result = users_service.find_user_by_id(user.id, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)
    
    def test_findUser_byId_returnsNone_when_userNotFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.find_user_by_id(user.id, mock_db)
        self.assertIsNone(result)
    
    def test_findUser_byToken_returnsUser_when_userFound(self):
        user = fake_user()
        token = users_service.generate_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        result = users_service.find_user_by_token(token, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)
    
    def test_findUser_byToken_returnsNone_when_userNotFound(self):
        user = fake_user()
        token = users_service.generate_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.find_user_by_token(token, mock_db)
        self.assertIsNone(result)
        
    def test_isUserAuthenticated_returnsTrue_when_userFound(self):
        user = fake_user()
        token = users_service.generate_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertTrue(result)
        
    def test_isUserAuthenticated_returnsFalse_when_userNotFound(self):
        user = fake_user()
        token = users_service.generate_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertFalse(result)
        
    def test_isUser_Authenticated_returnsFalse_when_invalidToken(self):
        token = "I am an invalid token :)"
        mock_db = Mock(spec=database)
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertFalse(result)
        
    