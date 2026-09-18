from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import RoommatePost
from .forms import RoommatePostForm

def roommate_list(request):
    queryset = RoommatePost.objects.filter(is_active=True).select_related('user', 'user__profile')

    q = request.GET.get('q', '').strip()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(target_college__icontains=q) |
            Q(target_locality__icontains=q) |
            Q(target_city__icontains=q) |
            Q(about_me__icontains=q)
        )

    city = request.GET.get('city', '').strip()
    if city:
        queryset = queryset.filter(target_city__iexact=city)

    gender = request.GET.get('gender', '').strip()
    if gender:
        queryset = queryset.filter(gender_preference__in=[gender, 'ANY'])

    diet = request.GET.get('diet', '').strip()
    if diet:
        queryset = queryset.filter(dietary_preference__in=[diet, 'ANY'])

    sleep = request.GET.get('sleep', '').strip()
    if sleep:
        queryset = queryset.filter(sleep_schedule=sleep)

    smoking = request.GET.get('smoking', '').strip()
    if smoking:
        queryset = queryset.filter(smoking_habit=smoking)

    post_type = request.GET.get('post_type', '').strip()
    if post_type:
        queryset = queryset.filter(post_type=post_type)

    max_budget = request.GET.get('max_budget', '').strip()
    if max_budget and max_budget.isdigit():
        queryset = queryset.filter(budget_per_month__lte=float(max_budget))

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cities = RoommatePost.objects.filter(is_active=True).values_list('target_city', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'cities': cities,
        'current_q': q,
        'current_city': city,
        'current_gender': gender,
        'current_diet': diet,
        'current_sleep': sleep,
        'current_smoking': smoking,
        'current_post_type': post_type,
        'current_max_budget': max_budget,
        'total_count': queryset.count(),
    }
    return render(request, 'roommates/list.html', context)

def roommate_detail(request, pk):
    post = get_object_or_404(RoommatePost.objects.select_related('user', 'user__profile'), pk=pk)
    
    # Similar roommate posts nearby
    similar_posts = RoommatePost.objects.filter(
        is_active=True,
        target_city=post.target_city
    ).exclude(pk=post.pk)[:3]

    context = {
        'post': post,
        'similar_posts': similar_posts,
    }
    return render(request, 'roommates/detail.html', context)

@login_required
def roommate_create(request):
    if request.method == 'POST':
        form = RoommatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Your roommate finding request is live! Students can now contact you directly.")
            return redirect('roommate_detail', pk=post.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        initial = {}
        if hasattr(request.user, 'profile'):
            initial['contact_phone'] = request.user.profile.phone
            initial['contact_whatsapp'] = request.user.profile.whatsapp_number or request.user.profile.phone
            initial['target_college'] = request.user.profile.college_name
        form = RoommatePostForm(initial=initial)

    return render(request, 'roommates/form.html', {'form': form, 'title': 'Find a Roommate / Flatmate (Zero Brokerage)'})

@login_required
def roommate_edit(request, pk):
    post = get_object_or_404(RoommatePost, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RoommatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Your post has been updated.")
            return redirect('roommate_detail', pk=post.pk)
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = RoommatePostForm(instance=post)

    return render(request, 'roommates/form.html', {'form': form, 'title': 'Edit Roommate Posting', 'post': post})

@login_required
def roommate_delete(request, pk):
    post = get_object_or_404(RoommatePost, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.info(request, "Roommate posting removed.")
        return redirect('dashboard')
    return render(request, 'roommates/confirm_delete.html', {'post': post})
