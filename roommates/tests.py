from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from roommates.models import RoommatePost

class RoommatesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = User.objects.create_user(username='student_rm', password='password123')
        self.post = RoommatePost.objects.create(
            user=self.student,
            post_type='NEED_ROOM',
            title='DU Student Seeking Roommate',
            target_college='Delhi University',
            target_city='New Delhi',
            target_locality='Kamla Nagar',
            budget_per_month=Decimal('7500.00'),
            gender_preference='MALE',
            occupancy_type='SHARED_ROOM',
            dietary_preference='VEG',
            smoking_habit='NON_SMOKER',
            sleep_schedule='EARLY_BIRD',
            study_vibe='QUIET',
            about_me='2nd year commerce student, friendly and calm.',
            contact_phone='9876543210',
            is_active=True,
        )

    def test_roommate_list_renders(self):
        response = self.client.get('/roommates/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DU Student Seeking Roommate')

    def test_roommate_filter_by_diet(self):
        response = self.client.get('/roommates/?diet=VEG')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DU Student Seeking Roommate')

    def test_create_roommate_post(self):
        self.client.login(username='student_rm', password='password123')
        response = self.client.post('/roommates/post/', {
            'post_type': 'HAVE_ROOM',
            'title': '1 Bed Available in 2BHK',
            'target_college': 'IIT Delhi',
            'target_city': 'New Delhi',
            'target_locality': 'Hauz Khas',
            'budget_per_month': '9000',
            'gender_preference': 'MALE',
            'occupancy_type': 'PRIVATE_ROOM',
            'dietary_preference': 'ANY',
            'smoking_habit': 'NON_SMOKER',
            'sleep_schedule': 'NIGHT_OWL',
            'study_vibe': 'BALANCED',
            'about_me': 'Great flat right next to IIT gate.',
            'contact_phone': '9112233445',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RoommatePost.objects.filter(title='1 Bed Available in 2BHK').exists())
