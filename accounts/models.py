from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Student / Room Seeker'),
        ('OWNER', 'Hostel / PG Owner'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=15, blank=True)
    whatsapp_number = models.CharField(max_length=15, blank=True)
    college_name = models.CharField(max_length=200, blank=True, help_text="e.g. Delhi University, IIT Bombay, Christ University")
    course = models.CharField(max_length=100, blank=True, help_text="e.g. B.Tech Computer Science, MBA, B.Com")
    year_of_study = models.CharField(max_length=50, blank=True, help_text="e.g. 1st Year, 2nd Year, Final Year")
    bio = models.TextField(blank=True, help_text="Brief introduction about yourself")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified_student = models.BooleanField(default=False, help_text="Verified via student ID card")
    is_verified_owner = models.BooleanField(default=False, help_text="Verified property ownership")
    id_card_proof = models.ImageField(upload_to='proofs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
