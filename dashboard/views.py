from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from listings.models import HostelListing, VisitRequest, SavedListing
from roommates.models import RoommatePost

@login_required
def dashboard_home(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    # Owner Data
    my_listings = HostelListing.objects.filter(owner=user).prefetch_related('amenities')
    incoming_visits = VisitRequest.objects.filter(listing__owner=user).select_related('listing', 'student').order_by('-created_at')

    # Student Data
    my_visits = VisitRequest.objects.filter(student=user).select_related('listing', 'listing__owner').order_by('-created_at')
    saved_items = SavedListing.objects.filter(user=user).select_related('listing')
    my_roommate_posts = RoommatePost.objects.filter(user=user).order_by('-created_at')

    context = {
        'profile': profile,
        'my_listings': my_listings,
        'incoming_visits': incoming_visits,
        'my_visits': my_visits,
        'saved_items': saved_items,
        'my_roommate_posts': my_roommate_posts,
        'active_tab': request.GET.get('tab', 'overview'),
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def toggle_listing_status(request, listing_id):
    listing = get_object_or_404(HostelListing, pk=listing_id, owner=request.user)
    if request.method == 'POST':
        listing.is_active = not listing.is_active
        listing.save()
        status_str = "Active (Live on Portal)" if listing.is_active else "Inactive (Hidden)"
        messages.success(request, f"'{listing.title}' is now {status_str}.")
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def update_visit_status(request, visit_id):
    visit = get_object_or_404(VisitRequest, pk=visit_id)
    # Check if the current user is the owner of the listing
    if visit.listing.owner != request.user and not request.user.is_staff:
        messages.error(request, "Permission denied.")
        return redirect('dashboard')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['ACCEPTED', 'DECLINED', 'COMPLETED']:
            visit.status = new_status
            visit.save()
            messages.success(request, f"Visit request status updated to '{visit.get_status_display()}'.")
    return redirect('dashboard')
