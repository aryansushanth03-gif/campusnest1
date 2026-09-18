from django.db import models
from django.contrib.auth.models import User

class RoommatePost(models.Model):
    POST_TYPES = [
        ('HAVE_ROOM', 'I Have a Room / Flat (Need Roommate)'),
        ('NEED_ROOM', 'I Need a Room / Looking to Team Up'),
    ]

    GENDER_PREFERENCES = [
        ('MALE', 'Male Roommates Only'),
        ('FEMALE', 'Female Roommates Only'),
        ('ANY', 'Any Gender Welcome'),
    ]

    OCCUPANCY_TYPES = [
        ('SHARED_ROOM', 'Twin Sharing in 1 Room'),
        ('PRIVATE_ROOM', 'Private Bedroom in Shared Flat'),
        ('ANY', 'Open to Either'),
    ]

    DIET_CHOICES = [
        ('VEG', 'Vegetarian Only'),
        ('NON_VEG', 'Non-Vegetarian Friendly'),
        ('EGGETARIAN', 'Eggetarian'),
        ('ANY', 'No Dietary Preference'),
    ]

    SMOKING_CHOICES = [
        ('NON_SMOKER', 'Strictly Non-Smoker'),
        ('BALCONY', 'Balcony / Outdoor Only'),
        ('SMOKER', 'Smoker Friendly'),
    ]

    SLEEP_CHOICES = [
        ('EARLY_BIRD', 'Early Bird (Up before 7 AM)'),
        ('NIGHT_OWL', 'Night Owl (Active past midnight)'),
        ('FLEXIBLE', 'Flexible Schedule'),
    ]

    STUDY_VIBES = [
        ('QUIET', 'Quiet & Study Focused'),
        ('BALANCED', 'Balanced (Study & Hangouts)'),
        ('SOCIAL', 'Social & Friendly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roommate_posts')
    post_type = models.CharField(max_length=15, choices=POST_TYPES, default='NEED_ROOM')
    title = models.CharField(max_length=200, help_text="e.g. 2nd Year DU Student looking for flatmate in Kamla Nagar")
    target_college = models.CharField(max_length=200, help_text="University or College you attend")
    target_city = models.CharField(max_length=100, default='New Delhi')
    target_locality = models.CharField(max_length=150, help_text="Preferred locality or area")
    
    budget_per_month = models.DecimalField(max_digits=10, decimal_places=2, help_text="Max monthly budget per person in ₹")
    gender_preference = models.CharField(max_length=10, choices=GENDER_PREFERENCES, default='MALE')
    occupancy_type = models.CharField(max_length=15, choices=OCCUPANCY_TYPES, default='SHARED_ROOM')

    # Lifestyle & Habits
    dietary_preference = models.CharField(max_length=15, choices=DIET_CHOICES, default='ANY')
    smoking_habit = models.CharField(max_length=15, choices=SMOKING_CHOICES, default='NON_SMOKER')
    sleep_schedule = models.CharField(max_length=15, choices=SLEEP_CHOICES, default='FLEXIBLE')
    study_vibe = models.CharField(max_length=15, choices=STUDY_VIBES, default='BALANCED')

    about_me = models.TextField(help_text="Introduce your course, year, lifestyle, and preferences in a flatmate")
    contact_phone = models.CharField(max_length=15)
    contact_whatsapp = models.CharField(max_length=15, blank=True)
    available_from = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} (₹{int(self.budget_per_month)}/mo)"

    @property
    def whatsapp_url(self):
        number = self.contact_whatsapp or self.contact_phone
        clean_number = "".join(filter(str.isdigit, number))
        if len(clean_number) == 10:
            clean_number = "91" + clean_number
        message = f"Hi {self.user.first_name or self.user.username}! I saw your roommate posting on CampusNest: '{self.title}'. I'd like to connect and see if we're a good match!"
        import urllib.parse
        return f"https://wa.me/{clean_number}?text={urllib.parse.quote(message)}"
