from django.test import TestCase, Client
from django.contrib.auth.models import User
from accounts.models import UserProfile

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_as_student(self):
        response = self.client.post('/accounts/register/', {
            'username': 'student_test',
            'first_name': 'Test',
            'last_name': 'Student',
            'email': 'student@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'STUDENT',
            'phone': '9876543210',
            'whatsapp_number': '9876543210',
            'college_name': 'Delhi University',
            'course': 'B.Sc Computer Science',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='student_test')
        self.assertEqual(user.profile.role, 'STUDENT')
        self.assertEqual(user.profile.college_name, 'Delhi University')
        self.assertEqual(user.profile.phone, '9876543210')

    def test_user_registration_as_owner(self):
        response = self.client.post('/accounts/register/', {
            'username': 'owner_test',
            'first_name': 'Owner',
            'last_name': 'Test',
            'email': 'owner@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': 'OWNER',
            'phone': '9988776655',
            'whatsapp_number': '9988776655',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='owner_test')
        self.assertEqual(user.profile.role, 'OWNER')

    def test_login_and_logout(self):
        user = User.objects.create_user(username='loginuser', password='password123')
        # Login
        response = self.client.post('/accounts/login/', {
            'username': 'loginuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

        # Logout
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)
