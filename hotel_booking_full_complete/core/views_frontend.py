from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.http import HttpResponseForbidden
from .models import User, Hotel, RoomType, Booking


# --------------------
# HOME PAGE
# --------------------
def home(request):
    return render(request, "home.html")


# --------------------
# REGISTER
# --------------------
def register_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        User.objects.create(
            email=email,
            password_hash=make_password(password)
        )
        messages.success(request, "Account created! Please login.")
        return redirect("login")

    return render(request, "register.html")


# --------------------
# LOGIN
# --------------------
def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        if not check_password(password, user.password_hash):
            messages.error(request, "Invalid email or password")
            return redirect("login")

        request.session["user_id"] = str(user.id)
        messages.success(request, "Logged in successfully!")
        return redirect("hotels")

    return render(request, "login.html")


# --------------------
# LOGOUT
# --------------------
def logout_page(request):
    request.session.flush()
    return redirect("login")


# --------------------
# HOTELS LIST PAGE
# --------------------
def hotels_page(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels.html", {"hotels": hotels})


# --------------------
# HOTEL DETAIL PAGE
# --------------------
def hotel_detail_page(request, hotel_id):
    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return redirect("hotels")

    rooms = RoomType.objects.filter(hotel=hotel)

    return render(request, "hotel_detail.html", {
        "hotel": hotel,
        "rooms": rooms
    })


# --------------------
# BOOKING PAGE (FORM)
# --------------------
def booking_page(request, hotel_id):
    if "user_id" not in request.session:
        return HttpResponseForbidden("Login required to book rooms.")

    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return redirect("hotels")

    if request.method == "POST":
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")

        user = User.objects.get(id=request.session["user_id"])

        booking = Booking.objects.create(
            user=user,
            hotel=hotel,
            checkin_date=checkin,
            checkout_date=checkout,
            booking_reference=f"BK-{user.id.hex[:6]}-{hotel.id.hex[:6]}",
            total_amount=1000,
            currency="INR",
            status="confirmed",
            created_at=timezone.now()
        )

        return redirect(f"/booking-success/?ref={booking.booking_reference}")

    return render(request, "book.html", {"hotel": hotel})


# --------------------
# BOOKING SUCCESS PAGE
# --------------------
def booking_success(request):
    ref = request.GET.get("ref")
    return render(request, "booking_success.html", {"ref": ref})
