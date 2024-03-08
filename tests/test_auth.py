import unittest
from app.services import auth_service

class TestAuthService(unittest.TestCase):

    def test_register_user(self):
        # Assuming register_user returns the user ID upon successful registration
        user_id = auth_service.register_user('testuser', 'password123', 'patient', 'test@example.com', 'Test User')
        self.assertIsNotNone(user_id)

    def test_login_user(self):
        # Test login with correct credentials
        user_id = auth_service.login_user('testuser', 'password123')
        self.assertIsNotNone(user_id)

        # Test login with incorrect credentials
        user_id = auth_service.login_user('testuser', 'wrongpassword')
        self.assertIsNone(user_id)

    def test_generate_token(self):
        # Assuming generate_token returns a non-empty string (the token)
        token = auth_service.generate_token(1)  # Pass a valid user ID
        self.assertTrue(token)

if __name__ == '__main__':
    unittest.main()
