from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Amenity(models.Model):
    name = models.CharField(max_length=60, unique=True)
    icon_class = models.CharField(max_length=60, default='bi bi-check-circle', help_text="Bootstrap Icon class, e.g., bi bi-wifi")

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ['name']

    def __str__(self):
        return self.name

class HostelListing(models.Model):
    PROPERTY_TYPES = [
        ('HOSTEL', 'Student Hostel'),
        ('PG', 'Paying Guest (PG)'),
        ('FLAT', 'Shared Student Flat'),
        ('ROOM', 'Private Room'),
    ]

    GENDER_CHOICES = [
        ('BOYS', 'Boys Only'),
        ('GIRLS', 'Girls Only'),
        ('COED', 'Co-Ed / Unisex'),
    ]

    ROOM_SHARING_CHOICES = [
        ('SINGLE', 'Single Occupancy (1 Bed)'),
        ('DOUBLE', 'Double Sharing (2 Beds)'),
        ('TRIPLE', 'Triple Sharing (3 Beds)'),
        ('FOUR_PLUS', '4+ Sharing'),
        ('FULL_FLAT', 'Entire Apartment / Flat'),
    ]

    FOOD_CHOICES = [
        ('INCLUDED_3X', 'All 3 Meals Included (Breakfast, Lunch, Dinner)'),
        ('INCLUDED_2X', '2 Meals Included (Breakfast & Dinner)'),
        ('BREAKFAST_ONLY', 'Breakfast Only Included'),
        ('MESS_AVAILABLE_EXTRA', 'Mess Available at Extra Charge'),
        ('SELF_COOKING', 'Self-Cooking Allowed / Kitchen Access'),
        ('NO_FOOD', 'No Food Facility'),
    ]

    FOOD_TYPES = [
        ('VEG_ONLY', 'Pure Vegetarian'),
        ('VEG_NONVEG', 'Veg & Non-Veg Available'),
        ('JAIN_AVAILABLE', 'Jain Food Available'),
        ('NA', 'Not Applicable / Self Cook'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    property_type = models.CharField(max_length=15, choices=PROPERTY_TYPES, default='PG')
    gender_preference = models.CharField(max_length=10, choices=GENDER_CHOICES, default='BOYS')
    room_sharing = models.CharField(max_length=15, choices=ROOM_SHARING_CHOICES, default='DOUBLE')

    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monthly rent per student in ₹")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Refundable deposit in ₹")
    maintenance_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Monthly maintenance in ₹ (0 if included)")
    notice_period_days = models.PositiveIntegerField(default=30)

    food_facility = models.CharField(max_length=25, choices=FOOD_CHOICES, default='INCLUDED_2X')
    food_type = models.CharField(max_length=20, choices=FOOD_TYPES, default='VEG_NONVEG')
    curfew_time = models.CharField(max_length=50, default='10:30 PM', help_text="e.g. 10:00 PM, 11:00 PM, 24x7 Entry")

    address = models.TextField()
    locality = models.CharField(max_length=150, help_text="e.g. North Campus, Koramangala, Kothrud")
    city = models.CharField(max_length=100, default='New Delhi')
    pincode = models.CharField(max_length=10, blank=True)
    nearby_college = models.CharField(max_length=200, help_text="Primary nearby university/college")
    distance_to_college_km = models.DecimalField(max_digits=4, decimal_places=1, default=0.5, help_text="Distance in KM")
    nearest_metro_bus = models.CharField(max_length=150, blank=True, help_text="e.g. GTB Nagar Metro Station (300m)")

    description = models.TextField()
    house_rules = models.TextField(
        blank=True,
        default="1. Gate closes at designated curfew time.\n2. Outside visitors permitted in lounge area.\n3. Maintain cleanliness in shared spaces.\n4. No smoking or alcohol allowed on premises."
    )

    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15)
    contact_whatsapp = models.CharField(max_length=15, blank=True)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name='listings')
    featured_image = models.ImageField(upload_to='hostels/', blank=True, null=True)
    
    is_verified = models.BooleanField(default=True, help_text="Verified zero-brokerage property")
    zero_brokerage_guarantee = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.locality}-{self.city}")
            slug = base_slug
            counter = 1
            while HostelListing.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}-{uuid.uuid4().hex[:4]}"
                counter += 1
            self.slug = slug
        if not self.contact_person and self.owner:
            self.contact_person = self.owner.get_full_name() or self.owner.username
        if not self.contact_whatsapp and self.contact_phone:
            self.contact_whatsapp = self.contact_phone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.locality}, {self.city} (₹{int(self.rent_per_month)}/mo)"

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 4.8  # Default high starting trust score for verified properties

    @property
    def review_count(self):
        return self.reviews.count()

    @property
    def whatsapp_url(self):
        number = self.contact_whatsapp or self.contact_phone
        clean_number = "".join(filter(str.isdigit, number))
        if len(clean_number) == 10:
            clean_number = "91" + clean_number
        message = f"Hello! I found your listing '{self.title}' on CampusNest (0% Brokerage Portal). I am a student interested in scheduling a visit or discussing room availability."
        import urllib.parse
        return f"https://wa.me/{clean_number}?text={urllib.parse.quote(message)}"

class ListingImage(models.Model):
    listing = models.ForeignKey(HostelListing, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='hostels/gallery/')
    caption = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"

class VisitRequest(models.Model):
    SLOT_CHOICES = [
        ('MORNING', 'Morning (09:00 AM - 12:00 PM)'),
        ('AFTERNOON', 'Afternoon (12:00 PM - 04:00 PM)'),
        ('EVENING', 'Evening (04:00 PM - 07:30 PM)'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending Owner Confirmation'),
        ('ACCEPTED', 'Visit Confirmed'),
        ('DECLINED', 'Declined'),
        ('COMPLETED', 'Visit Completed'),
    ]

    listing = models.ForeignKey(HostelListing, on_delete=models.CASCADE, related_name='visit_requests')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_visits')
    visit_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=SLOT_CHOICES, default='EVENING')
    student_name = models.CharField(max_length=100)
    student_phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Visit for {self.listing.title} by {self.student_name} on {self.visit_date}"

class ListingReview(models.Model):
    listing = models.ForeignKey(HostelListing, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostel_reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    cleanliness_rating = models.PositiveSmallIntegerField(default=5)
    food_rating = models.PositiveSmallIntegerField(default=5)
    safety_rating = models.PositiveSmallIntegerField(default=5)
    title = models.CharField(max_length=150)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ review by {self.student.username} for {self.listing.title}"

class SavedListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(HostelListing, on_delete=models.CASCADE, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"

class ListingReport(models.Model):
    REASON_CHOICES = [
        ('BROKER_FOUND', 'Demanding Brokerage Fee / Broker Posing as Owner'),
        ('FAKE_PHOTOS', 'Fake Photos or Misleading Room Description'),
        ('WRONG_PRICE', 'Price Quoted Differently from Portal'),
        ('UNAVAILABLE', 'Room Already Occupied / Unavailable'),
        ('SAFETY_ISSUE', 'Safety or Harassment Concern'),
        ('OTHER', 'Other Violation'),
    ]

    listing = models.ForeignKey(HostelListing, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.CharField(max_length=30, choices=REASON_CHOICES)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report on {self.listing.title}: {self.get_reason_display()}"
