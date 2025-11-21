from django.db import models
import uuid

def gen_uuid():
    return uuid.uuid4()

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=64)

class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    code = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    preferred_language = models.CharField(max_length=10, blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    iso_code = models.CharField(max_length=8)
    name = models.CharField(max_length=200)

class Region(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    star_rating = models.SmallIntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    main_phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='draft')

class HotelDetail(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='detail')
    description = models.TextField(blank=True, null=True)
    checkin_time = models.TimeField(blank=True, null=True)
    checkout_time = models.TimeField(blank=True, null=True)
    language_support = models.CharField(max_length=255, blank=True, null=True)

class HotelPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='photos')
    url = models.CharField(max_length=1000)
    caption = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(default=0)

class HotelFacility(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class HotelFacilityMap(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    facility = models.ForeignKey(HotelFacility, on_delete=models.CASCADE)

class RoomType(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    max_adults = models.IntegerField(default=2)
    max_children = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=64, blank=True, null=True)
    floor = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=32, default='available')

class RoomPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='photos')
    url = models.CharField(max_length=1000)
    caption = models.CharField(max_length=255, blank=True, null=True)

class RoomAmenity(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

class RoomAmenityMap(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    amenity = models.ForeignKey(RoomAmenity, on_delete=models.CASCADE)

class RatePlan(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)
    prepayment_required = models.BooleanField(default=False)
    refundable = models.BooleanField(default=True)
    cancellation_policy_id = models.CharField(max_length=255, blank=True, null=True)

class RatePlanRate(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    rate_plan = models.ForeignKey(RatePlan, on_delete=models.CASCADE, related_name='rates')
    date_from = models.DateField()
    date_to = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default='USD')
    min_stay = models.IntegerField(default=1)
    max_stay = models.IntegerField(default=30)

class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    iso_code = models.CharField(max_length=8)
    symbol = models.CharField(max_length=8)
    exchange_rate_to_base = models.DecimalField(max_digits=12, decimal_places=6, default=1.0)

class Tax(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    apply_to = models.CharField(max_length=32, default='room')

class TaxRule(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

class InventoryCalendar(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()
    available_count = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=64, unique=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default='USD')
    status = models.CharField(max_length=32, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class BookingRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    rate_plan = models.ForeignKey(RatePlan, on_delete=models.SET_NULL, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

class BookingPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    provider_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=32, default='initiated')
    method = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=128)
    pdf_url = models.CharField(max_length=1000, blank=True, null=True)
    issued_at = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

class Refund(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    booking_payment = models.ForeignKey(BookingPayment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, default='processing')

class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=16, choices=(('percent','percent'),('fixed','fixed')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    usage_limit = models.IntegerField(default=1)

class CouponClaim(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    claimed_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(blank=True, null=True)

class Promotion(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    rules = models.JSONField(default=dict, blank=True)

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=32, default='published')

class ReviewPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='photos')
    url = models.CharField(max_length=1000)

class QuestionAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class CompareList(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CompareItem(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    compare_list = models.ForeignKey(CompareList, on_delete=models.CASCADE, related_name='items')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

class AvailabilityRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
    num_rooms = models.IntegerField(default=1)
    status = models.CharField(max_length=32, default='open')

class BookingAuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    payload = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    body = models.TextField()
    delivered = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)

class PushToken(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    platform = models.CharField(max_length=50, blank=True, null=True)

class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=32, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

class SupportComment(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    contact_info = models.TextField(blank=True, null=True)
    contract_id = models.CharField(max_length=255, blank=True, null=True)

class VendorContract(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    terms = models.TextField(blank=True, null=True)

class HotelManager(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, blank=True, null=True)

class Staff(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=128, blank=True, null=True)
    employment_status = models.CharField(max_length=64, blank=True, null=True)

class Shift(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    start_time = models.TimeField()
    end_time = models.TimeField()

class ShiftAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()

class CleaningSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()
    assigned_staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=64, default='pending')

class HousekeepingTask(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    schedule = models.ForeignKey(CleaningSchedule, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=128)
    status = models.CharField(max_length=64, default='open')
    notes = models.TextField(blank=True, null=True)

class InventoryLock(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    date = models.DateField()
    locked_by = models.CharField(max_length=128, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

class SeoMetadata(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    entity_type = models.CharField(max_length=64)
    entity_id = models.CharField(max_length=128)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)

class Setting(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    value = models.JSONField(default=dict, blank=True)

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    entity_type = models.CharField(max_length=128)
    entity_id = models.CharField(max_length=128)
    action = models.CharField(max_length=128)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AnalyticsEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=128)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PageView(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    path = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Affiliate(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

class AffiliateCommission(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    affiliate = models.ForeignKey(Affiliate, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(blank=True, null=True)

class LoyaltyProgram(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    rules = models.JSONField(default=dict, blank=True)

class LoyaltyAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE)
    points_balance = models.IntegerField(default=0)

class LoyaltyTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    account = models.ForeignKey(LoyaltyAccount, on_delete=models.CASCADE)
    points_delta = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
