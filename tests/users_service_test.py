from unittest import mock
from data.models import User, UserLoginData, UserRegisterData
from mariadb import IntegrityError
from services import users_service
from unittest.mock import Mock
from data import database
import unittest

def fake_user(id: int = 1, username: str = "emko", password: str = "Pass123!", 
              is_admin: int = 1, avatar_url: str | None = None,
              created_at: str = "2025-05-19 10:20:03") -> Mock:
    
    mock_user = Mock(spec=User)
    mock_user.id = id
    mock_user.username = username
    mock_user.password = password
    mock_user.is_admin = is_admin
    mock_user.avatar_url = avatar_url
    mock_user.created_at = created_at
    return mock_user

class UsersServiceTest(unittest.TestCase):
        
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
        # Simulate IntegrityError when username is taken
        mock_db.insert_query.side_effect = IntegrityError()

        register_data = UserRegisterData(username=user.username, password=user.password, is_admin=user.is_admin)
        result = users_service.register_user(register_data, mock_db)
        self.assertIsNone(result)
        
    def test_loginUser_returnsUser_when_userFound(self):
        user = fake_user()
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin, user.avatar_url, user.created_at)]
        
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
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin, user.avatar_url, user.created_at)]
        
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
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin, user.avatar_url, user.created_at)]
        
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
        token = users_service.encode_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin, user.avatar_url, user.created_at)]
        
        result = users_service.find_user_by_token(token, mock_db)
        self.assertIsInstance(result, User)
        self.assertEqual(result.username, user.username)
    
    def test_findUser_byToken_returnsNone_when_userNotFound(self):
        user = fake_user()
        token = users_service.encode_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.find_user_by_token(token, mock_db)
        self.assertIsNone(result)
        
    def test_isUserAuthenticated_returnsTrue_when_userFound(self):
        user = fake_user()
        token = users_service.encode_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = [(user.id, user.username, user.password, user.is_admin)]
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertTrue(result)
        
    def test_isUserAuthenticated_returnsFalse_when_userNotFound(self):
        user = fake_user()
        token = users_service.encode_user_token(user)
        mock_db = Mock(spec=database)
        mock_db.read_query.return_value = []
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertFalse(result)
        
    def test_isUser_Authenticated_returnsFalse_when_invalidToken(self):
        token = "I am an invalid token :)"
        mock_db = Mock(spec=database)
        
        result = users_service.is_user_authenticated(token, mock_db)
        self.assertFalse(result)
        
    