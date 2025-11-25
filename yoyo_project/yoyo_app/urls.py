from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('api/hotels/', views.hotels_near_location, name="hotels_near_location"),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('hotel/<int:address_id>/', views.hotel_detail, name='hotel_detail'),
]
