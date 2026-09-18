from django.contrib import admin
from .models import HostelListing, ListingImage, Amenity, VisitRequest, ListingReview, SavedListing, ListingReport

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 2

@admin.register(HostelListing)
class HostelListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'gender_preference', 'room_sharing', 'rent_per_month', 'city', 'locality', 'is_verified', 'is_active', 'view_count')
    list_filter = ('property_type', 'gender_preference', 'room_sharing', 'city', 'is_verified', 'is_active')
    search_fields = ('title', 'locality', 'city', 'nearby_college', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ListingImageInline]

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')
    search_fields = ('name',)

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('listing', 'student', 'visit_date', 'time_slot', 'student_phone', 'status', 'created_at')
    list_filter = ('status', 'visit_date', 'time_slot')
    search_fields = ('student__username', 'student_name', 'student_phone', 'listing__title')

@admin.register(ListingReview)
class ListingReviewAdmin(admin.ModelAdmin):
    list_display = ('listing', 'student', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('listing__title', 'student__username', 'title', 'comment')

@admin.register(SavedListing)
class SavedListingAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'created_at')
    search_fields = ('user__username', 'listing__title')

@admin.register(ListingReport)
class ListingReportAdmin(admin.ModelAdmin):
    list_display = ('listing', 'reported_by', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('listing__title', 'details')
