from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'college_name', 'is_verified_student', 'is_verified_owner', 'created_at')
    list_filter = ('role', 'is_verified_student', 'is_verified_owner')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'college_name', 'phone')
