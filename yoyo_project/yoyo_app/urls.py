from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('profile/', views.profile, name='profile'),    
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('api/hotels/', views.hotels_near_location, name="hotels_near_location"),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('hotel/<int:address_id>/', views.hotel_detail, name='hotel_detail'),
    path('accounts/', include('allauth.urls')),
    path('bookings_history/',views.bookings_history,name='bookings_history'),
    path('api/bookings/',views.get_bookings_api,name='get_bookings_api'),
    path('payment/<int:hotel_id>/<int:room_id>/<int:adults>/',views.payment,name='payment'),
    path('successfull_payment/<int:hotel_id>/<int:room_id>/', views.successfull_payment, name='successfull_payment'),
]
