from django.urls import path
from . import views_frontend as v

urlpatterns = [
    path("", v.home, name="home"),

    path("register/", v.register_page, name="register"),
    path("login/", v.login_page, name="login"),
    path("logout/", v.logout_page, name="logout"),

    path("hotels/", v.hotels_page, name="hotels"),
    path("hotels/<uuid:hotel_id>/", v.hotel_detail_page, name="hotel_detail"),

    path("book/<uuid:hotel_id>/", v.booking_page, name="book"),

    path("booking-success/", v.booking_success, name="booking_success"),
]
