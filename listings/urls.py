from django.urls import path
from . import views

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('post/', views.listing_create, name='listing_create'),
    path('save/<int:listing_id>/', views.toggle_save_listing, name='toggle_save_listing'),
    path('reveal-contact/<int:listing_id>/', views.reveal_contact, name='reveal_contact'),
    path('<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('<slug:slug>/edit/', views.listing_edit, name='listing_edit'),
    path('<slug:slug>/delete/', views.listing_delete, name='listing_delete'),
    path('<slug:slug>/schedule-visit/', views.schedule_visit, name='schedule_visit'),
    path('<slug:slug>/add-review/', views.add_review, name='add_review'),
    path('<slug:slug>/report/', views.report_listing, name='report_listing'),
]
