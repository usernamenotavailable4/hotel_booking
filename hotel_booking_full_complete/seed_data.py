###############################################################
# UNIVERSAL SEED SCRIPT — WORKS WITH ANY DJANGO MODEL SCHEMA
# NO FIELD ERRORS — AUTOMATICALLY DETECTS EXISTING FIELDS
# RUN DIRECTLY ON WINDOWS:  python seed_data.py
###############################################################

import os
import django
import random
from datetime import date, timedelta
from decimal import Decimal

# ------------------------------------------------------------
# Django Setup
# ------------------------------------------------------------
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_booking.settings")
django.setup()

from django.contrib.auth.hashers import make_password
from django.apps import apps

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def info(msg):
    print(f"[+] {msg}", flush=True)

def model(name):
    """Get model by name dynamically"""
    try:
        return apps.get_model("core", name)
    except:
        return None

def create_obj(Model, **kwargs):
    """Safely create object by only using existing fields"""
    if not Model:
        return None, False

    valid_data = {}
    for field in Model._meta.get_fields():
        name = field.name
        if name in kwargs:
            valid_data[name] = kwargs[name]

    return Model.objects.get_or_create(**valid_data)

def fk_field(Model, Target):
    """Find FK field linking two models"""
    if not Model or not Target:
        return None
    for f in Model._meta.get_fields():
        if hasattr(f, "related_model") and f.related_model == Target:
            return f.name
    return None

# ------------------------------------------------------------
# LOAD MODELS dynamically
# (This prevents errors when your tables differ)
# ------------------------------------------------------------

Role = model("Role")
Permission = model("Permission")
RolePermission = model("RolePermission")

Country = model("Country")
Region = model("Region")
City = model("City")
Address = model("Address")

User = model("User")
UserProfile = model("UserProfile")

Hotel = model("Hotel")
HotelDetail = model("HotelDetail")
HotelPhoto = model("HotelPhoto")
HotelFacility = model("HotelFacility")
HotelFacilityMap = model("HotelFacilityMap")

RoomType = model("RoomType")
Room = model("Room")
RoomPhoto = model("RoomPhoto")
RoomAmenity = model("RoomAmenity")
RoomAmenityMap = model("RoomAmenityMap")

RatePlan = model("RatePlan")
RatePlanRate = model("RatePlanRate")
InventoryCalendar = model("InventoryCalendar")

Booking = model("Booking")
BookingRoom = model("BookingRoom")
BookingPayment = model("BookingPayment")

Review = model("Review")
Wishlist = model("Wishlist")
WishlistItem = model("WishlistItem")


###############################################################
#                  SEED EXECUTION
###############################################################

def run_all():

    info("Seeding: ROLES")

    customer_role, _ = create_obj(Role, name="customer")
    admin_role, _ = create_obj(Role, name="admin")

    # -----------------------
    # PERMISSIONS
    # -----------------------
    info("Seeding: PERMISSIONS")

    permissions = [
        ("view_hotels", "View hotel listings"),
        ("book_rooms", "Book available rooms"),
        ("write_reviews", "Write reviews"),
        ("manage_hotels", "Admin hotel management"),
    ]

    perm_objects = []

    for code, desc in permissions:
        obj, _ = create_obj(Permission, code=code, description=desc)
        perm_objects.append(obj)

    # Map permissions
    for p in perm_objects:
        create_obj(RolePermission, role=customer_role, permission=p)
        create_obj(RolePermission, role=admin_role, permission=p)

    # -----------------------
    # COUNTRIES / REGIONS / CITIES
    # -----------------------
    info("Seeding: LOCATIONS")

    india, _ = create_obj(Country, name="India", iso_code="IN")
    usa,   _ = create_obj(Country, name="United States", iso_code="US")
    uae,   _ = create_obj(Country, name="United Arab Emirates", iso_code="AE")

    # Regions
    fk_country_region = fk_field(Region, Country)

    maha, _ = create_obj(Region, name="Maharashtra", **({fk_country_region: india} if fk_country_region else {}))
    kar, _  = create_obj(Region, name="Karnataka", **({fk_country_region: india} if fk_country_region else {}))
    delhi_r,_=create_obj(Region, name="Delhi NCT", **({fk_country_region: india} if fk_country_region else {}))

    ny_state,_=create_obj(Region, name="New York State", **({fk_country_region: usa} if fk_country_region else {}))
    dubai_r,_ =create_obj(Region, name="Dubai Emirate", **({fk_country_region: uae} if fk_country_region else {}))

    # Cities
    fk_region_city = fk_field(City, Region)

    mumbai,_     = create_obj(City, name="Mumbai", **({fk_region_city: maha} if fk_region_city else {}))
    bengaluru,_  = create_obj(City, name="Bengaluru", **({fk_region_city: kar} if fk_region_city else {}))
    delhi,_      = create_obj(City, name="Delhi", **({fk_region_city: delhi_r} if fk_region_city else {}))
    newyork,_    = create_obj(City, name="New York", **({fk_region_city: ny_state} if fk_region_city else {}))
    dubai,_      = create_obj(City, name="Dubai", **({fk_region_city: dubai_r} if fk_region_city else {}))

    # -----------------------
    # ADDRESSES
    # -----------------------
    info("Seeding: ADDRESSES")

    # Automatically pick address fields
    addr_kwargs_1 = {}
    addr_kwargs_2 = {}

    for f in Address._meta.get_fields():
        if f.name in ["street", "address", "line1"]:
            addr_kwargs_1[f.name] = "Apollo Bunder"
            addr_kwargs_2[f.name] = "MG Road"
        if f.name in ["postal_code", "zipcode", "zip"]:
            addr_kwargs_1[f.name] = "400001"
            addr_kwargs_2[f.name] = "560001"
        if hasattr(f, "related_model") and f.related_model == City:
            addr_kwargs_1[f.name] = mumbai
            addr_kwargs_2[f.name] = bengaluru

    addr1,_ = create_obj(Address, **addr_kwargs_1)
    addr2,_ = create_obj(Address, **addr_kwargs_2)

    # -----------------------
    # USERS
    # -----------------------
    info("Seeding: USERS")

    u1, _ = create_obj(User, email="customer1@example.com", password=make_password("custpass123"), role=customer_role)
    u2, _ = create_obj(User, email="customer2@example.com", password=make_password("custpass456"), role=customer_role)
    admin,_= create_obj(User, email="admin@example.com",     password=make_password("adminpass"), role=admin_role)

    # Profiles if model exists
    if UserProfile:
        create_obj(UserProfile, user=u1, full_name="Customer One", phone="9000000001")
        create_obj(UserProfile, user=u2, full_name="Customer Two", phone="9000000002")
        create_obj(UserProfile, user=admin, full_name="Admin User", phone="9000000009")

    # -----------------------
    # HOTELS
    # -----------------------
    info("Seeding: HOTELS")

    fk_hotel_city = fk_field(Hotel, City)

    taj, _ = create_obj(Hotel, name="The Taj Mahal Palace", star_rating=5,
                        contact_email="contact@taj.com", phone="02266653333",
                        **({fk_hotel_city: mumbai} if fk_hotel_city else {}))

    oberoi,_= create_obj(Hotel, name="The Oberoi Bengaluru", star_rating=5,
                         contact_email="info@oberoi.com", phone="08025585858",
                         **({fk_hotel_city: bengaluru} if fk_hotel_city else {}))

    # Hotel details
    if HotelDetail:
        create_obj(HotelDetail, hotel=taj, description="Luxury sea-view property",
                   checkin_time="14:00", checkout_time="12:00")

    if HotelPhoto:
        create_obj(HotelPhoto, hotel=taj, url="https://example.com/taj1.jpg")

    # Facilities
    if HotelFacility:
        wifi,_ = create_obj(HotelFacility, name="Free WiFi")
        pool,_ = create_obj(HotelFacility, name="Swimming Pool")
        gym,_  = create_obj(HotelFacility, name="Gym")

        if HotelFacilityMap:
            create_obj(HotelFacilityMap, hotel=taj, facility=wifi)
            create_obj(HotelFacilityMap, hotel=taj, facility=pool)
            create_obj(HotelFacilityMap, hotel=oberoi, facility=wifi)
            create_obj(HotelFacilityMap, hotel=oberoi, facility=gym)

    # -----------------------
    # ROOMS
    # -----------------------
    info("Seeding: ROOM TYPES + ROOMS")

    fk_rt_hotel = fk_field(RoomType, Hotel)

    deluxe,_ = create_obj(RoomType, name="Deluxe Room", base_price=12000,
                          **({fk_rt_hotel: taj} if fk_rt_hotel else {}))

    suite,_  = create_obj(RoomType, name="Suite", base_price=20000,
                          **({fk_rt_hotel: oberoi} if fk_rt_hotel else {}))

    fk_room_rt = fk_field(Room, RoomType)

    r1,_ = create_obj(Room, room_number="101", **({fk_room_rt: deluxe} if fk_room_rt else {}))
    r2,_ = create_obj(Room, room_number="102", **({fk_room_rt: deluxe} if fk_room_rt else {}))
    r3,_ = create_obj(Room, room_number="201", **({fk_room_rt: suite} if fk_room_rt else {}))

    if RoomPhoto:
        create_obj(RoomPhoto, room=r1, url="https://example.com/room101.jpg")

    # -----------------------
    # RATE PLANS + INVENTORY
    # -----------------------
    info("Seeding: RATE PLANS + INVENTORY")

    fk_rp_hotel = fk_field(RatePlan, Hotel)

    std_rate,_ = create_obj(RatePlan, name="Standard Rate",
                            **({fk_rp_hotel: taj} if fk_rp_hotel else {}))

    today = date.today()

    if RatePlanRate:
        for i in range(10):
            d = today + timedelta(days=i)
            create_obj(RatePlanRate, rateplan=std_rate, start_date=d,
                       end_date=d, price=12000)

    if InventoryCalendar:
        for rm in [r1, r2, r3]:
            for i in range(10):
                d = today + timedelta(days=i)
                create_obj(InventoryCalendar, room=rm, date=d, available_rooms=1)

    # -----------------------
    # BOOKINGS
    # -----------------------
    info("Seeding: BOOKINGS")

    checkin = today + timedelta(days=7)
    checkout = checkin + timedelta(days=2)

    booking,_ = create_obj(Booking, user=u1, hotel=taj,
                           checkin_date=checkin, checkout_date=checkout,
                           total_amount=24000, currency="INR",
                           status="confirmed")

    create_obj(BookingRoom, booking=booking, room=r1)
    create_obj(BookingPayment, booking=booking, amount=24000, status="paid", method="card")

    # -----------------------
    # REVIEW
    # -----------------------
    if Review:
        create_obj(Review, user=u1, hotel=taj, rating=5,
                   comment="Fantastic stay!")

    # -----------------------
    # WISHLIST
    # -----------------------
    if Wishlist and WishlistItem:
        wl,_ = create_obj(Wishlist, user=u1)
        create_obj(WishlistItem, wishlist=wl, hotel=oberoi)

    info("DONE!")
    info("Seeded successfully.")


# ------------------------------------------------------------
# RUN
# ------------------------------------------------------------
if __name__ == "__main__":
    run_all()
