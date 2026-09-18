from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('listing/<int:listing_id>/toggle/', views.toggle_listing_status, name='toggle_listing_status'),
    path('visit/<int:visit_id>/status/', views.update_visit_status, name='update_visit_status'),
]
