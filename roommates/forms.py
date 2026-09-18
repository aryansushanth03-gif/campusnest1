from django import forms
from .models import RoommatePost

class RoommatePostForm(forms.ModelForm):
    class Meta:
        model = RoommatePost
        fields = [
            'post_type', 'title', 'target_college', 'target_city', 'target_locality',
            'budget_per_month', 'gender_preference', 'occupancy_type',
            'dietary_preference', 'smoking_habit', 'sleep_schedule', 'study_vibe',
            'about_me', 'contact_phone', 'contact_whatsapp', 'available_from'
        ]
        widgets = {
            'post_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2nd Year DU student looking for chill flatmate in Kamla Nagar'}),
            'target_college': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Delhi University / SRCC / IIT Delhi'}),
            'target_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. New Delhi, Bengaluru, Pune'}),
            'target_locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Hudson Lane, Koramangala'}),
            'budget_per_month': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly budget in ₹'}),
            'gender_preference': forms.Select(attrs={'class': 'form-select'}),
            'occupancy_type': forms.Select(attrs={'class': 'form-select'}),
            'dietary_preference': forms.Select(attrs={'class': 'form-select'}),
            'smoking_habit': forms.Select(attrs={'class': 'form-select'}),
            'sleep_schedule': forms.Select(attrs={'class': 'form-select'}),
            'study_vibe': forms.Select(attrs={'class': 'form-select'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell potential flatmates about yourself: hobbies, course, habits, what kind of vibe you like...'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calling number'}),
            'contact_whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
