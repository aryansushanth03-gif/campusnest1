from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from listings.models import HostelListing, Amenity, VisitRequest, SavedListing, ListingReview

class ListingsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username='owner1', password='pass123', email='owner1@test.com')
        self.student = User.objects.create_user(username='student1', password='pass123', email='student1@test.com')

        self.wifi = Amenity.objects.create(name='High-Speed Wi-Fi', icon_class='bi bi-wifi')
        self.ac = Amenity.objects.create(name='Air Conditioner (AC)', icon_class='bi bi-snow')

        self.listing = HostelListing.objects.create(
            owner=self.owner,
            title='Campus Comfort Boys PG',
            property_type='PG',
            gender_preference='BOYS',
            room_sharing='DOUBLE',
            rent_per_month=Decimal('8000.00'),
            security_deposit=Decimal('8000.00'),
            food_facility='INCLUDED_2X',
            food_type='VEG_NONVEG',
            address='123 University Road',
            locality='North Campus',
            city='New Delhi',
            nearby_college='Delhi University',
            distance_to_college_km=Decimal('0.5'),
            description='Super clean accommodation with great food.',
            contact_phone='9876543210',
            is_active=True,
        )
        self.listing.amenities.add(self.wifi, self.ac)

    def test_listing_slug_generation(self):
        self.assertTrue(self.listing.slug.startswith('campus-comfort-boys-pg'))

    def test_homepage_renders_successfully(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campus Comfort Boys PG')
        self.assertContains(response, '0% BROKERAGE')

    def test_listing_search_and_filter(self):
        # Search by keyword
        response = self.client.get('/hostels/?q=Delhi+University')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campus Comfort Boys PG')

        # Filter by gender
        response = self.client.get('/hostels/?gender=GIRLS')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Campus Comfort Boys PG')

        # Filter by price range
        response = self.client.get('/hostels/?max_price=9000')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campus Comfort Boys PG')

    def test_schedule_visit(self):
        self.client.login(username='student1', password='pass123')
        response = self.client.post(f'/hostels/{self.listing.slug}/schedule-visit/', {
            'visit_date': str(date.today()),
            'time_slot': 'EVENING',
            'student_name': 'Student One',
            'student_phone': '9123456780',
            'notes': 'Looking forward to visiting.'
        })
        self.assertEqual(response.status_code, 302)
        visit = VisitRequest.objects.filter(listing=self.listing, student=self.student).first()
        self.assertIsNotNone(visit)
        self.assertEqual(visit.status, 'PENDING')
        self.assertEqual(visit.student_name, 'Student One')

    def test_toggle_save_listing(self):
        self.client.login(username='student1', password='pass123')
        # Save
        response = self.client.post(f'/hostels/save/{self.listing.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'saved')
        self.assertTrue(SavedListing.objects.filter(user=self.student, listing=self.listing).exists())

        # Unsave
        response = self.client.post(f'/hostels/save/{self.listing.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'removed')
        self.assertFalse(SavedListing.objects.filter(user=self.student, listing=self.listing).exists())

    def test_reveal_contact_api(self):
        response = self.client.get(f'/hostels/reveal-contact/{self.listing.id}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['contact_phone'], '9876543210')
        self.assertTrue('wa.me' in data['whatsapp_url'])
