from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('STUDENT', '🎓 Student / Room Seeker (Zero Brokerage)'),
        ('OWNER', '🏠 Hostel / PG Owner (Direct Listing)'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='STUDENT')
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. 9876543210', 'class': 'form-control'}))
    whatsapp_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. 9876543210 (optional)', 'class': 'form-control'}))
    college_name = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. Delhi University / IIT / Christ Univ', 'class': 'form-control'}))
    course = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. B.Tech CSE / MBA / B.Com', 'class': 'form-control'}))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Re-enter your password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unique username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['phone', 'whatsapp_number', 'college_name', 'course', 'year_of_study', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'year_of_study': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2nd Year'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
