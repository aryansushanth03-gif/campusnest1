import urllib.request
import os
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from accounts.models import UserProfile
from listings.models import HostelListing, Amenity, ListingReview, SavedListing, VisitRequest
from roommates.models import RoommatePost

class Command(BaseCommand):
    help = "Seed realistic sample data for CampusNest NoBroker Student Portal"

    def handle(self, *args, **options):
        self.stdout.write("Starting CampusNest database seeding...")

        # 1. Amenities
        amenities_data = [
            ("High-Speed Wi-Fi", "bi bi-wifi"),
            ("Air Conditioner (AC)", "bi bi-snow"),
            ("Attached Washroom", "bi bi-door-closed"),
            ("Geyser / Hot Water", "bi bi-droplet-half"),
            ("RO Drinking Water", "bi bi-cup-straw"),
            ("Power Backup", "bi bi-lightning-charge"),
            ("Laundry / Washing Machine", "bi bi-basket"),
            ("Daily Housekeeping", "bi bi-stars"),
            ("CCTV 24x7 Security", "bi bi-camera-video"),
            ("Study Table & Ergonomic Chair", "bi bi-book"),
            ("Biometric Entry", "bi bi-fingerprint"),
            ("Common Refrigerator", "bi bi-archive"),
            ("Balcony / Ventilation", "bi bi-tree"),
            ("Gym / Indoor Games", "bi bi-activity"),
        ]

        amenity_objs = {}
        for name, icon in amenities_data:
            amen, _ = Amenity.objects.get_or_create(name=name, defaults={'icon_class': icon})
            amenity_objs[name] = amen
        self.stdout.write(self.style.SUCCESS(f"Created/Verified {len(amenity_objs)} amenities."))

        # 2. Superuser / Admin
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@campusnest.local', 'admin123')
            admin_user.first_name = 'Admin'
            admin_user.last_name = 'Manager'
            admin_user.save()
            admin_profile = admin_user.profile
            admin_profile.role = 'OWNER'
            admin_profile.phone = '9876500000'
            admin_profile.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin123)."))

        # 3. Sample Owners
        owners_info = [
            {
                'username': 'sharma_hostels',
                'first_name': 'Ramesh',
                'last_name': 'Sharma',
                'email': 'sharma.hostels@gmail.com',
                'phone': '9811223344',
                'role': 'OWNER',
                'is_verified': True,
                'bio': 'Verified student accommodation provider in North Campus Delhi for 12+ years. Zero brokerage guaranteed.'
            },
            {
                'username': 'stanza_nest',
                'first_name': 'Kavita',
                'last_name': 'Reddy',
                'email': 'kavita.reddy@gmail.com',
                'phone': '9988776655',
                'role': 'OWNER',
                'is_verified': True,
                'bio': 'Premium student living spaces near major universities in Bangalore and Pune with hygienic food.'
            },
            {
                'username': 'royal_stays',
                'first_name': 'Vikram',
                'last_name': 'Mehta',
                'email': 'vikram.stays@gmail.com',
                'phone': '9822334455',
                'role': 'OWNER',
                'is_verified': True,
                'bio': 'Clean, secure, and modern student flats and PGs in Mumbai & Delhi.'
            }
        ]

        owners = {}
        for info in owners_info:
            user, created = User.objects.get_or_create(
                username=info['username'],
                defaults={
                    'first_name': info['first_name'],
                    'last_name': info['last_name'],
                    'email': info['email']
                }
            )
            if created:
                user.set_password('owner123')
                user.save()
            profile = user.profile
            profile.role = 'OWNER'
            profile.phone = info['phone']
            profile.whatsapp_number = info['phone']
            profile.is_verified_owner = info['is_verified']
            profile.bio = info['bio']
            profile.save()
            owners[info['username']] = user

        # 4. Sample Students
        students_info = [
            {
                'username': 'aarav_du',
                'first_name': 'Aarav',
                'last_name': 'Sharma',
                'email': 'aarav.sharma@du.ac.in',
                'phone': '9711223344',
                'college': 'Delhi University (Hindu College)',
                'course': 'B.Com (Hons)',
                'year': '2nd Year',
                'bio': 'Commerce student at DU. Non-smoker, early riser, love basketball and quiet study sessions.'
            },
            {
                'username': 'ananya_iit',
                'first_name': 'Ananya',
                'last_name': 'Patel',
                'email': 'ananya.p@iitb.ac.in',
                'phone': '9822114477',
                'college': 'IIT Bombay',
                'course': 'B.Tech Computer Science',
                'year': '3rd Year',
                'bio': 'Tech enthusiast, love coding hackathons, vegetarian, night owl.'
            },
            {
                'username': 'rohan_christ',
                'first_name': 'Rohan',
                'last_name': 'Gupta',
                'email': 'rohan.g@christ.edu',
                'phone': '9655443322',
                'college': 'Christ University, Bangalore',
                'course': 'BBA Finance',
                'year': '1st Year',
                'bio': 'Fresher looking for a sociable, clean flatmate near Koramangala.'
            },
            {
                'username': 'sneha_pune',
                'first_name': 'Sneha',
                'last_name': 'Kulkarni',
                'email': 'sneha.k@fergusson.edu',
                'phone': '9544332211',
                'college': 'Fergusson College, Pune',
                'course': 'M.Sc Biotechnology',
                'year': 'Final Year',
                'bio': 'Masters student. Prefer a peaceful study-friendly environment.'
            },
        ]

        students = {}
        for s in students_info:
            user, created = User.objects.get_or_create(
                username=s['username'],
                defaults={
                    'first_name': s['first_name'],
                    'last_name': s['last_name'],
                    'email': s['email']
                }
            )
            if created:
                user.set_password('student123')
                user.save()
            profile = user.profile
            profile.role = 'STUDENT'
            profile.phone = s['phone']
            profile.whatsapp_number = s['phone']
            profile.college_name = s['college']
            profile.course = s['course']
            profile.year_of_study = s['year']
            profile.is_verified_student = True
            profile.bio = s['bio']
            profile.save()
            students[s['username']] = user

        self.stdout.write(self.style.SUCCESS("Created sample owners and verified students."))

        # 5. Realistic Hostel & PG Listings
        listings_data = [
            {
                'owner': owners['sharma_hostels'],
                'title': 'Oxford Scholar Boys PG & Residency',
                'property_type': 'PG',
                'gender_preference': 'BOYS',
                'room_sharing': 'DOUBLE',
                'rent_per_month': Decimal('9500.00'),
                'security_deposit': Decimal('9500.00'),
                'maintenance_charge': Decimal('0.00'),
                'food_facility': 'INCLUDED_3X',
                'food_type': 'VEG_NONVEG',
                'curfew_time': '10:30 PM',
                'address': 'Plot 42, Hudson Lane, Near Guru Tegh Bahadur Khalsa College',
                'locality': 'Hudson Lane (North Campus)',
                'city': 'New Delhi',
                'pincode': '110009',
                'nearby_college': 'Delhi University (North Campus)',
                'distance_to_college_km': Decimal('0.4'),
                'nearest_metro_bus': 'GTB Nagar Metro (Yellow Line - 350m)',
                'description': 'A premium, student-focused boys accommodation within walking distance of DU North Campus colleges. High-speed 300 Mbps mesh Wi-Fi, hygienic 3-time daily meals prepared by in-house chefs, daily housekeeping, RO drinking water, and dedicated study desks in every room. 0% Brokerage.',
                'house_rules': '1. Main gate locks at 10:30 PM for security.\n2. In-room quiet hours from 11:00 PM to 7:00 AM.\n3. Common dining area must be used for meals.\n4. Strict anti-ragging and zero alcohol policy.',
                'contact_phone': '9811223344',
                'amenities': [
                    "High-Speed Wi-Fi", "Air Conditioner (AC)", "Attached Washroom",
                    "Geyser / Hot Water", "RO Drinking Water", "Power Backup",
                    "Laundry / Washing Machine", "Daily Housekeeping", "CCTV 24x7 Security",
                    "Study Table & Ergonomic Chair", "Biometric Entry"
                ]
            },
            {
                'owner': owners['stanza_nest'],
                'title': 'Lotus Haven Girls Luxury Student Hostel',
                'property_type': 'HOSTEL',
                'gender_preference': 'GIRLS',
                'room_sharing': 'DOUBLE',
                'rent_per_month': Decimal('12000.00'),
                'security_deposit': Decimal('12000.00'),
                'maintenance_charge': Decimal('0.00'),
                'food_facility': 'INCLUDED_3X',
                'food_type': 'VEG_ONLY',
                'curfew_time': '10:00 PM',
                'address': '5th Block, Opposite Jyoti Nivas College Road, Koramangala',
                'locality': 'Koramangala 5th Block',
                'city': 'Bengaluru',
                'pincode': '560095',
                'nearby_college': 'Christ University, Bangalore',
                'distance_to_college_km': Decimal('0.8'),
                'nearest_metro_bus': 'Koramangala Sony World Signal (300m)',
                'description': 'High-security girls hostel featuring biometric access, 24x7 female warden on campus, CCTV surveillance, nutritious North & South Indian meals, air-conditioned rooms with ergonomic study spaces, and high-speed fiber internet. Ideal for Christ and St. Joseph students.',
                'house_rules': '1. Entry strictly monitored with biometric system.\n2. Night-out requires prior parental confirmation via SMS.\n3. Female guests allowed in visitor lounge during daylight hours.',
                'contact_phone': '9988776655',
                'amenities': [
                    "High-Speed Wi-Fi", "Air Conditioner (AC)", "Attached Washroom",
                    "Geyser / Hot Water", "RO Drinking Water", "Power Backup",
                    "Laundry / Washing Machine", "Daily Housekeeping", "CCTV 24x7 Security",
                    "Study Table & Ergonomic Chair", "Biometric Entry", "Gym / Indoor Games"
                ]
            },
            {
                'owner': owners['royal_stays'],
                'title': 'Powai Techies Shared 3BHK Student Flat',
                'property_type': 'FLAT',
                'gender_preference': 'COED',
                'room_sharing': 'SINGLE',
                'rent_per_month': Decimal('16500.00'),
                'security_deposit': Decimal('20000.00'),
                'maintenance_charge': Decimal('1000.00'),
                'food_facility': 'SELF_COOKING',
                'food_type': 'NA',
                'curfew_time': 'No Curfew / 24x7 Access',
                'address': 'Tower B, Hiranandani Gardens, Near IIT Main Gate, Powai',
                'locality': 'Powai',
                'city': 'Mumbai',
                'pincode': '400076',
                'nearby_college': 'IIT Bombay / Powai',
                'distance_to_college_km': Decimal('0.5'),
                'nearest_metro_bus': 'IIT Main Gate Bus Stop (200m) / Kanjurmarg Station (1.8km)',
                'description': 'Fully furnished 3BHK high-rise apartment for university students and tech interns. Private single occupancy bedroom with split AC, modular kitchen equipped with refrigerator, microwave, gas connection, and washing machine. Zero curfew for university scholars.',
                'house_rules': '1. Keep music within respectable decibels after 11 PM.\n2. Maintain cleanliness in shared kitchen and living lounge.\n3. Flatmate mutual respect and shared utility expenses.',
                'contact_phone': '9822334455',
                'amenities': [
                    "High-Speed Wi-Fi", "Air Conditioner (AC)", "Attached Washroom",
                    "Geyser / Hot Water", "RO Drinking Water", "Power Backup",
                    "Laundry / Washing Machine", "Common Refrigerator", "Balcony / Ventilation",
                    "Gym / Indoor Games"
                ]
            },
            {
                'owner': owners['sharma_hostels'],
                'title': 'Fergusson Heritage Co-Ed PG & Stays',
                'property_type': 'PG',
                'gender_preference': 'COED',
                'room_sharing': 'TRIPLE',
                'rent_per_month': Decimal('6800.00'),
                'security_deposit': Decimal('5000.00'),
                'maintenance_charge': Decimal('0.00'),
                'food_facility': 'INCLUDED_2X',
                'food_type': 'VEG_NONVEG',
                'curfew_time': '11:00 PM',
                'address': 'Lane 3, Behind Fergusson College Campus, FC Road',
                'locality': 'FC Road / Deccan Gymkhana',
                'city': 'Pune',
                'pincode': '411004',
                'nearby_college': 'Pune University / Fergusson',
                'distance_to_college_km': Decimal('0.3'),
                'nearest_metro_bus': 'Deccan Gymkhana Metro Station (400m)',
                'description': 'Pocket-friendly student accommodation situated right behind Fergusson College. Ideal for Pune University, BMCC, and Fergusson students. Includes morning breakfast and wholesome dinner, power backup, high-speed Wi-Fi, and study rooms.',
                'house_rules': '1. Curfew at 11:00 PM.\n2. Weekly laundry schedule.\n3. Smoking prohibited on premises.',
                'contact_phone': '9811223344',
                'amenities': [
                    "High-Speed Wi-Fi", "Geyser / Hot Water", "RO Drinking Water",
                    "Power Backup", "Laundry / Washing Machine", "Daily Housekeeping",
                    "Study Table & Ergonomic Chair", "CCTV 24x7 Security"
                ]
            },
            {
                'owner': owners['stanza_nest'],
                'title': 'Miranda Elite Girls PG (Single & Twin Sharing)',
                'property_type': 'PG',
                'gender_preference': 'GIRLS',
                'room_sharing': 'SINGLE',
                'rent_per_month': Decimal('14500.00'),
                'security_deposit': Decimal('15000.00'),
                'maintenance_charge': Decimal('0.00'),
                'food_facility': 'INCLUDED_3X',
                'food_type': 'VEG_NONVEG',
                'curfew_time': '10:15 PM',
                'address': '18, Bungalow Road, Kamla Nagar Market, North Campus',
                'locality': 'Kamla Nagar',
                'city': 'New Delhi',
                'pincode': '110007',
                'nearby_college': 'Delhi University (North Campus)',
                'distance_to_college_km': Decimal('0.6'),
                'nearest_metro_bus': 'Vishwavidyalaya Metro (600m)',
                'description': 'High-end student residency located in the heart of Kamla Nagar. Close to Miranda House, SRCC, St. Stephens, and KMC. Individual attached bathrooms with hot geysers, split ACs, high-speed fiber internet, and 4-course hygienic daily meals.',
                'house_rules': '1. Biometric punch entry for all residents.\n2. Parental consent for overnight stays.\n3. Courteous behavior in communal dining hall.',
                'contact_phone': '9988776655',
                'amenities': [
                    "High-Speed Wi-Fi", "Air Conditioner (AC)", "Attached Washroom",
                    "Geyser / Hot Water", "RO Drinking Water", "Power Backup",
                    "Laundry / Washing Machine", "Daily Housekeeping", "CCTV 24x7 Security",
                    "Study Table & Ergonomic Chair", "Biometric Entry", "Common Refrigerator"
                ]
            },
            {
                'owner': owners['royal_stays'],
                'title': 'Koramangala Greenview Student Hostel',
                'property_type': 'HOSTEL',
                'gender_preference': 'BOYS',
                'room_sharing': 'DOUBLE',
                'rent_per_month': Decimal('8500.00'),
                'security_deposit': Decimal('8500.00'),
                'maintenance_charge': Decimal('0.00'),
                'food_facility': 'INCLUDED_2X',
                'food_type': 'VEG_NONVEG',
                'curfew_time': '11:00 PM',
                'address': '80 Feet Road, Near Sony World Signal, 4th Block',
                'locality': 'Koramangala',
                'city': 'Bengaluru',
                'pincode': '560034',
                'nearby_college': 'Christ University, Bangalore',
                'distance_to_college_km': Decimal('1.1'),
                'nearest_metro_bus': 'Koramangala Bus Depot (400m)',
                'description': 'Spacious and breezy rooms overlooking lush trees. Ideal student hub with high-speed internet, dedicated study room, South Indian and North Indian mess options, and laundry facility. 100% No Brokerage fee.',
                'house_rules': '1. Gate closes at 11:00 PM.\n2. Mutual respect among roommates.',
                'contact_phone': '9822334455',
                'amenities': [
                    "High-Speed Wi-Fi", "Attached Washroom", "Geyser / Hot Water",
                    "RO Drinking Water", "Power Backup", "Laundry / Washing Machine",
                    "Study Table & Ergonomic Chair", "Balcony / Ventilation"
                ]
            }
        ]

        created_listings = []
        for l_data in listings_data:
            amenity_names = l_data.pop('amenities')
            listing, created = HostelListing.objects.get_or_create(
                title=l_data['title'],
                locality=l_data['locality'],
                defaults=l_data
            )
            # Add amenities
            for a_name in amenity_names:
                if a_name in amenity_objs:
                    listing.amenities.add(amenity_objs[a_name])
            listing.save()
            created_listings.append(listing)

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_listings)} verified hostel & PG listings."))

        # 6. Sample Student Reviews
        reviews_data = [
            (created_listings[0], students['aarav_du'], 5, 5, 5, 5, "Best PG in Hudson Lane!", "Stayed here during my entire 1st year at Hindu College. The food is surprisingly good and hygienic, unlike most PGs. Wi-Fi speed is rock solid for online study and projects. Owner Sharma ji is very supportive and zero brokerage was a huge relief!"),
            (created_listings[1], students['sneha_pune'], 5, 5, 5, 5, "Super safe and friendly warden", "The security at Lotus Haven is top tier. Biometric entry and caring warden made my parents feel totally reassured. Also walking distance to Christ University!"),
            (created_listings[2], students['ananya_iit'], 5, 5, 4, 5, "Amazing flat near IIT Bombay", "Hiranandani location is unmatched. Flat is fully loaded with modern appliances. Ideal for serious engineering students who want peace and focus."),
            (created_listings[3], students['rohan_christ'], 4, 4, 4, 4, "Value for money in Pune", "Great location on FC Road, food is decent, and roommates are all university students. Highly recommend for freshers on a budget."),
        ]

        for listing, student, rating, c_rat, f_rat, s_rat, title, comment in reviews_data:
            ListingReview.objects.get_or_create(
                listing=listing,
                student=student,
                defaults={
                    'rating': rating,
                    'cleanliness_rating': c_rat,
                    'food_rating': f_rat,
                    'safety_rating': s_rat,
                    'title': title,
                    'comment': comment,
                }
            )

        # 7. Sample Saved Wishlists & Visits
        SavedListing.objects.get_or_create(user=students['aarav_du'], listing=created_listings[0])
        SavedListing.objects.get_or_create(user=students['aarav_du'], listing=created_listings[4])
        SavedListing.objects.get_or_create(user=students['ananya_iit'], listing=created_listings[2])

        VisitRequest.objects.get_or_create(
            listing=created_listings[0],
            student=students['aarav_du'],
            defaults={
                'visit_date': date.today() + timedelta(days=2),
                'time_slot': 'EVENING',
                'student_name': 'Aarav Sharma',
                'student_phone': '9711223344',
                'notes': 'Would love to check room 204 and mess food during dinner time.',
                'status': 'ACCEPTED'
            }
        )

        VisitRequest.objects.get_or_create(
            listing=created_listings[1],
            student=students['sneha_pune'],
            defaults={
                'visit_date': date.today() + timedelta(days=3),
                'time_slot': 'AFTERNOON',
                'student_name': 'Sneha Kulkarni',
                'student_phone': '9544332211',
                'notes': 'Visiting with my parents on Saturday afternoon.',
                'status': 'PENDING'
            }
        )

        # 8. Roommate Posts
        roommates_data = [
            {
                'user': students['aarav_du'],
                'post_type': 'NEED_ROOM',
                'title': 'DU North Campus Commerce Student Looking for Flatmate in Kamla Nagar',
                'target_college': 'Delhi University (Hindu College)',
                'target_city': 'New Delhi',
                'target_locality': 'Kamla Nagar / Hudson Lane',
                'budget_per_month': Decimal('8000.00'),
                'gender_preference': 'MALE',
                'occupancy_type': 'SHARED_ROOM',
                'dietary_preference': 'NON_VEG',
                'smoking_habit': 'NON_SMOKER',
                'sleep_schedule': 'EARLY_BIRD',
                'study_vibe': 'BALANCED',
                'about_me': 'Hey! I am Aarav, 2nd year B.Com (Hons) student at Hindu College. I am organized, calm, and respectful of personal space. Looking for a chilled flatmate who is focused on academics but also enjoys weekend chai walks in North Campus.',
                'contact_phone': '9711223344',
                'contact_whatsapp': '9711223344',
                'available_from': date.today() + timedelta(days=5),
            },
            {
                'user': students['ananya_iit'],
                'post_type': 'HAVE_ROOM',
                'title': '1 Private Room available in 3BHK Highrise flat in Powai near IIT Bombay',
                'target_college': 'IIT Bombay',
                'target_city': 'Mumbai',
                'target_locality': 'Powai (Hiranandani)',
                'budget_per_month': Decimal('15000.00'),
                'gender_preference': 'FEMALE',
                'occupancy_type': 'PRIVATE_ROOM',
                'dietary_preference': 'VEG',
                'smoking_habit': 'NON_SMOKER',
                'sleep_schedule': 'NIGHT_OWL',
                'study_vibe': 'QUIET',
                'about_me': 'CS student at IITB. We have 1 spacious master room open in our 3BHK flat. Fully furnished, split AC, maid for cooking and cleaning. Looking for a quiet, responsible student or intern who values clean spaces.',
                'contact_phone': '9822114477',
                'contact_whatsapp': '9822114477',
                'available_from': date.today() + timedelta(days=7),
            },
            {
                'user': students['rohan_christ'],
                'post_type': 'NEED_ROOM',
                'title': 'Christ University Fresher Looking to team up for 2BHK in Koramangala',
                'target_college': 'Christ University, Bangalore',
                'target_city': 'Bengaluru',
                'target_locality': 'Koramangala 4th / 5th Block',
                'budget_per_month': Decimal('10000.00'),
                'gender_preference': 'MALE',
                'occupancy_type': 'SHARED_ROOM',
                'dietary_preference': 'ANY',
                'smoking_habit': 'NON_SMOKER',
                'sleep_schedule': 'FLEXIBLE',
                'study_vibe': 'SOCIAL',
                'about_me': 'Joining BBA at Christ University Central Campus. I am super easy-going, love football and music. Want to find a fellow student to rent a decent 2BHK flat together to save on brokerage!',
                'contact_phone': '9655443322',
                'contact_whatsapp': '9655443322',
                'available_from': date.today() + timedelta(days=10),
            },
            {
                'user': students['sneha_pune'],
                'post_type': 'NEED_ROOM',
                'title': 'M.Sc Student Looking for Female Roommate near Fergusson College',
                'target_college': 'Fergusson College, Pune',
                'target_city': 'Pune',
                'target_locality': 'FC Road / Deccan',
                'budget_per_month': Decimal('7000.00'),
                'gender_preference': 'FEMALE',
                'occupancy_type': 'SHARED_ROOM',
                'dietary_preference': 'VEG',
                'smoking_habit': 'NON_SMOKER',
                'sleep_schedule': 'EARLY_BIRD',
                'study_vibe': 'QUIET',
                'about_me': 'Biotech postgraduate student at Fergusson. Quiet, clean, and disciplined. Looking for a vegetarian female student to share an apartment room nearby.',
                'contact_phone': '9544332211',
                'contact_whatsapp': '9544332211',
                'available_from': date.today() + timedelta(days=4),
            }
        ]

        for rm_data in roommates_data:
            RoommatePost.objects.get_or_create(
                user=rm_data['user'],
                title=rm_data['title'],
                defaults=rm_data
            )

        self.stdout.write(self.style.SUCCESS("Created sample roommate finder posts."))
        self.stdout.write(self.style.SUCCESS("All sample data seeded successfully!"))
