from django.contrib import admin
from .models import RoommatePost

@admin.register(RoommatePost)
class RoommatePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'post_type', 'target_college', 'target_city', 'budget_per_month', 'gender_preference', 'is_active', 'created_at')
    list_filter = ('post_type', 'gender_preference', 'occupancy_type', 'dietary_preference', 'target_city', 'is_active')
    search_fields = ('title', 'target_college', 'target_locality', 'target_city', 'user__username', 'about_me')
