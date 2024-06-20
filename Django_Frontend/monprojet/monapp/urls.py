from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-client/', views.client_create_view, name='create-client'),
    path('create-staff/', views.staff_create_view, name='create-staff'),
    path('create-staff-type/', views.staff_type_create_view, name='create-staff-type'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('success/', views.success, name='success'),
    path('view_staff/', views.view_staff, name='view_staff'),
    path('view_clients/', views.view_clients, name='view_clients'),
    path('view_staff_types/', views.view_staff_types, name='view_staff_types'),
]