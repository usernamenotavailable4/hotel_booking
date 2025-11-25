from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/hotels/', views.hotels_near_location, name="hotels_near_location"),
    path('hotel/<int:address_id>/', views.hotel_detail, name='hotel_detail'),
]
