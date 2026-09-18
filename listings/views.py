from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import (
    HostelListing, ListingImage, Amenity,
    VisitRequest, ListingReview, SavedListing, ListingReport
)
from .forms import HostelListingForm, VisitRequestForm, ListingReviewForm, ListingReportForm
from roommates.models import RoommatePost

def home(request):
    featured_listings = HostelListing.objects.filter(is_active=True).select_related('owner')[:6]
    recent_roommates = RoommatePost.objects.filter(is_active=True).select_related('user')[:4]
    
    # Popular college hubs for quick-click filters
    top_colleges = [
        'Delhi University (North Campus)',
        'IIT Delhi',
        'Christ University, Bangalore',
        'Pune University / Fergusson',
        'IIT Bombay / Powai',
        'Manipal University',
    ]

    total_listings = HostelListing.objects.filter(is_active=True).count()
    total_roommates = RoommatePost.objects.filter(is_active=True).count()

    user_saved_ids = []
    if request.user.is_authenticated:
        user_saved_ids = list(SavedListing.objects.filter(user=request.user).values_list('listing_id', flat=True))

    context = {
        'featured_listings': featured_listings,
        'recent_roommates': recent_roommates,
        'top_colleges': top_colleges,
        'total_listings': total_listings,
        'total_roommates': total_roommates,
        'user_saved_ids': user_saved_ids,
    }
    return render(request, 'home.html', context)

def listing_list(request):
    queryset = HostelListing.objects.filter(is_active=True).prefetch_related('amenities')

    # Keyword Search (college, locality, city, title)
    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(nearby_college__icontains=q) |
            Q(locality__icontains=q) |
            Q(city__icontains=q) |
            Q(description__icontains=q)
        )

    # City filter
    city = request.GET.get('city', '').strip()
    if city:
        queryset = queryset.filter(city__iexact=city)

    # College filter
    college = request.GET.get('college', '').strip()
    if college:
        queryset = queryset.filter(nearby_college__icontains=college)

    # Gender filter
    gender = request.GET.get('gender', '').strip()
    if gender in ['BOYS', 'GIRLS', 'COED']:
        queryset = queryset.filter(gender_preference=gender)

    # Sharing / Room type filter
    sharing = request.GET.get('sharing', '').strip()
    if sharing:
        queryset = queryset.filter(room_sharing=sharing)

    # Property type filter
    prop_type = request.GET.get('property_type', '').strip()
    if prop_type:
        queryset = queryset.filter(property_type=prop_type)

    # Food facility filter
    food = request.GET.get('food', '').strip()
    if food == 'included':
        queryset = queryset.filter(food_facility__in=['INCLUDED_3X', 'INCLUDED_2X', 'BREAKFAST_ONLY'])
    elif food:
        queryset = queryset.filter(food_facility=food)

    # Price range filter
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price and min_price.isdigit():
        queryset = queryset.filter(rent_per_month__gte=float(min_price))
    if max_price and max_price.isdigit():
        queryset = queryset.filter(rent_per_month__lte=float(max_price))

    # Amenities filter (multiple)
    selected_amenities = request.GET.getlist('amenity')
    if selected_amenities:
        for amen_id in selected_amenities:
            if amen_id.isdigit():
                queryset = queryset.filter(amenities__id=amen_id)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_asc':
        queryset = queryset.order_by('rent_per_month')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-rent_per_month')
    elif sort == 'distance':
        queryset = queryset.order_by('distance_to_college_km')
    else:  # newest
        queryset = queryset.order_by('-created_at')

    # Pagination: 9 per page
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_amenities = Amenity.objects.all()
    available_cities = HostelListing.objects.filter(is_active=True).values_list('city', flat=True).distinct()

    user_saved_ids = []
    if request.user.is_authenticated:
        user_saved_ids = list(SavedListing.objects.filter(user=request.user).values_list('listing_id', flat=True))

    context = {
        'page_obj': page_obj,
        'all_amenities': all_amenities,
        'available_cities': available_cities,
        'user_saved_ids': user_saved_ids,
        'selected_amenities': [int(a) for a in selected_amenities if a.isdigit()],
        'current_q': q,
        'current_city': city,
        'current_college': college,
        'current_gender': gender,
        'current_sharing': sharing,
        'current_prop_type': prop_type,
        'current_food': food,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_sort': sort,
        'total_count': queryset.count(),
    }
    return render(request, 'listings/list.html', context)

def listing_detail(request, slug):
    listing = get_object_or_404(HostelListing.objects.prefetch_related('amenities', 'additional_images', 'reviews__student'), slug=slug)
    
    # Increment view count
    HostelListing.objects.filter(pk=listing.pk).update(view_count=listing.view_count + 1)
    
    # Similar listings in the same city or near the same college
    similar_listings = HostelListing.objects.filter(
        is_active=True,
        city=listing.city
    ).exclude(pk=listing.pk)[:3]

    # Check if current user has saved this
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedListing.objects.filter(user=request.user, listing=listing).exists()

    # Forms
    visit_form = VisitRequestForm(initial={
        'student_name': request.user.get_full_name() or request.user.username if request.user.is_authenticated else '',
        'student_phone': request.user.profile.phone if request.user.is_authenticated and hasattr(request.user, 'profile') else ''
    })
    review_form = ListingReviewForm()
    report_form = ListingReportForm()

    context = {
        'listing': listing,
        'similar_listings': similar_listings,
        'is_saved': is_saved,
        'visit_form': visit_form,
        'review_form': review_form,
        'report_form': report_form,
    }
    return render(request, 'listings/detail.html', context)

@login_required
def schedule_visit(request, slug):
    listing = get_object_or_404(HostelListing, slug=slug)
    if request.method == 'POST':
        form = VisitRequestForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.listing = listing
            visit.student = request.user
            visit.save()
            messages.success(request, f"Visit request scheduled for {visit.visit_date}! The owner has been notified.")
        else:
            messages.error(request, "Could not schedule visit. Please check details.")
    return redirect('listing_detail', slug=slug)

@login_required
def add_review(request, slug):
    listing = get_object_or_404(HostelListing, slug=slug)
    if request.method == 'POST':
        form = ListingReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.listing = listing
            review.student = request.user
            review.save()
            messages.success(request, "Thank you! Your verified student review has been posted.")
        else:
            messages.error(request, "Failed to post review. Please fill all fields.")
    return redirect('listing_detail', slug=slug)

@login_required
def report_listing(request, slug):
    listing = get_object_or_404(HostelListing, slug=slug)
    if request.method == 'POST':
        form = ListingReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.listing = listing
            report.reported_by = request.user
            report.save()
            messages.warning(request, "Report submitted. Our moderation team will investigate this listing.")
        else:
            messages.error(request, "Failed to submit report.")
    return redirect('listing_detail', slug=slug)

@login_required
def listing_create(request):
    if request.method == 'POST':
        form = HostelListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            form.save_m2m()

            # Multiple images upload
            images = request.FILES.getlist('additional_images')
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)

            messages.success(request, f"'{listing.title}' has been successfully posted with 0% Brokerage!")
            return redirect('listing_detail', slug=listing.slug)
        else:
            messages.error(request, "Please resolve the form errors below.")
    else:
        # Pre-fill contact details from profile
        initial_data = {}
        if hasattr(request.user, 'profile'):
            initial_data['contact_person'] = request.user.get_full_name() or request.user.username
            initial_data['contact_phone'] = request.user.profile.phone
            initial_data['contact_whatsapp'] = request.user.profile.whatsapp_number or request.user.profile.phone
        form = HostelListingForm(initial=initial_data)

    return render(request, 'listings/form.html', {'form': form, 'title': 'Post a Student Hostel / PG (Zero Brokerage)'})

@login_required
def listing_edit(request, slug):
    listing = get_object_or_404(HostelListing, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = HostelListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            listing = form.save()
            
            # Additional images
            images = request.FILES.getlist('additional_images')
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)
                
            messages.success(request, "Listing updated successfully.")
            return redirect('listing_detail', slug=listing.slug)
        else:
            messages.error(request, "Please correct the errors.")
    else:
        form = HostelListingForm(instance=listing)

    return render(request, 'listings/form.html', {'form': form, 'title': f"Edit: {listing.title}", 'listing': listing})

@login_required
def listing_delete(request, slug):
    listing = get_object_or_404(HostelListing, slug=slug, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.info(request, "Listing has been removed.")
        return redirect('dashboard')
    return render(request, 'listings/confirm_delete.html', {'listing': listing})

@login_required
def toggle_save_listing(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(HostelListing, pk=listing_id)
        saved = SavedListing.objects.filter(user=request.user, listing=listing)
        if saved.exists():
            saved.delete()
            return JsonResponse({'status': 'removed', 'message': 'Removed from saved listings'})
        else:
            SavedListing.objects.create(user=request.user, listing=listing)
            return JsonResponse({'status': 'saved', 'message': 'Saved to your wishlist!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def reveal_contact(request, listing_id):
    """Zero-Brokerage direct contact reveal"""
    listing = get_object_or_404(HostelListing, pk=listing_id)
    return JsonResponse({
        'status': 'success',
        'contact_person': listing.contact_person,
        'contact_phone': listing.contact_phone,
        'whatsapp_url': listing.whatsapp_url,
    })
