from django import forms
from .models import HostelListing, VisitRequest, ListingReview, ListingReport, Amenity

class HostelListingForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'amenity-checkbox'}),
        required=False
    )

    class Meta:
        model = HostelListing
        fields = [
            'title', 'property_type', 'gender_preference', 'room_sharing',
            'rent_per_month', 'security_deposit', 'maintenance_charge', 'notice_period_days',
            'food_facility', 'food_type', 'curfew_time',
            'city', 'locality', 'address', 'pincode',
            'nearby_college', 'distance_to_college_km', 'nearest_metro_bus',
            'description', 'house_rules',
            'contact_person', 'contact_phone', 'contact_whatsapp',
            'amenities', 'featured_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Royal Oxford Boys PG & Student Hostel'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'gender_preference': forms.Select(attrs={'class': 'form-select'}),
            'room_sharing': forms.Select(attrs={'class': 'form-select'}),
            'rent_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly rent in ₹'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Refundable deposit in ₹'}),
            'maintenance_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly maintenance (0 if included)'}),
            'notice_period_days': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}),
            'food_facility': forms.Select(attrs={'class': 'form-select'}),
            'food_type': forms.Select(attrs={'class': 'form-select'}),
            'curfew_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10:30 PM or 24x7 Entry'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. New Delhi, Bengaluru, Pune'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. North Campus, Koramangala, Kothrud'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Full street address'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '110007'}),
            'nearby_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Delhi University / SRCC / IIT'}),
            'distance_to_college_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '0.5'}),
            'nearest_metro_bus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Vishwavidyalaya Metro Station (300m)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe rooms, study environment, hygiene, atmosphere...'}),
            'house_rules': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Key house rules (curfew, visitors, silence hours)'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner or Manager Name'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Calling Number'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number (for instant lead chats)'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = ['visit_date', 'time_slot', 'student_name', 'student_phone', 'notes']
        widgets = {
            'visit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'student_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your 10-digit Mobile Number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any question or preferred time (optional)...'}),
        }

class ListingReviewForm(forms.ModelForm):
    class Meta:
        model = ListingReview
        fields = ['rating', 'cleanliness_rating', 'food_rating', 'safety_rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(5, '5 Stars - Excellent'), (4, '4 Stars - Good'), (3, '3 Stars - Average'), (2, '2 Stars - Below Average'), (1, '1 Star - Poor')], attrs={'class': 'form-select'}),
            'cleanliness_rating': forms.Select(choices=[(5, '5/5 Clean'), (4, '4/5 Good'), (3, '3/5 Average'), (2, '2/5 Needs Work'), (1, '1/5 Poor')], attrs={'class': 'form-select'}),
            'food_rating': forms.Select(choices=[(5, '5/5 Delicious'), (4, '4/5 Healthy & Good'), (3, '3/5 Decent'), (2, '2/5 Bland'), (1, '1/5 Poor')], attrs={'class': 'form-select'}),
            'safety_rating': forms.Select(choices=[(5, '5/5 Very Safe & Secure'), (4, '4/5 Safe'), (3, '3/5 Moderate'), (2, '2/5 Low'), (1, '1/5 Unsafe')], attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summary of your stay (e.g. Great food & super fast WiFi)'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your genuine experience for other university students...'}),
        }

class ListingReportForm(forms.ModelForm):
    class Meta:
        model = ListingReport
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Provide details about this violation so our admin team can take action immediately...'}),
        }
