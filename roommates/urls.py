from django.urls import path
from . import views

urlpatterns = [
    path('', views.roommate_list, name='roommate_list'),
    path('post/', views.roommate_create, name='roommate_create'),
    path('<int:pk>/', views.roommate_detail, name='roommate_detail'),
    path('<int:pk>/edit/', views.roommate_edit, name='roommate_edit'),
    path('<int:pk>/delete/', views.roommate_delete, name='roommate_delete'),
]
