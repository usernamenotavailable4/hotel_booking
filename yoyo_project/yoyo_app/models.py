# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountEmailaddress(models.Model):
    email = models.CharField(max_length=254)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailaddress'
        unique_together = (('user', 'email'),)


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey('City', models.DO_NOTHING, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'address'


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    amenity_type = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amenity'


class AmenityMap(models.Model):
    amenity = models.ForeignKey(Amenity, models.DO_NOTHING)
    entity_type = models.CharField(max_length=32)
    entity_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'amenity_map'


class AnalyticsEvent(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    event_type = models.CharField(max_length=128, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'analytics_event'


class AuditLog(models.Model):
    entity_type = models.CharField(max_length=128, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=128, blank=True, null=True)
    performed_by = models.ForeignKey('User', models.DO_NOTHING, db_column='performed_by', blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit_log'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AvailabilityReq(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', models.DO_NOTHING, blank=True, null=True)
    date_from = models.DateField(blank=True, null=True)
    date_to = models.DateField(blank=True, null=True)
    num_rooms = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'availability_req'


class BookingAudit(models.Model):
    booking = models.ForeignKey('Bookings', models.DO_NOTHING)
    action = models.CharField(max_length=255, blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey('User', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_audit'


class BookingPayment(models.Model):
    booking = models.ForeignKey('Bookings', models.DO_NOTHING)
    provider_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=32, blank=True, null=True)
    method = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_payment'


class BookingRoom(models.Model):
    booking = models.ForeignKey('Bookings', models.DO_NOTHING)
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING, blank=True, null=True)
    rate_plan = models.ForeignKey('RatePlan', models.DO_NOTHING, blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'booking_room'


class Bookings(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', models.DO_NOTHING)
    booking_reference = models.CharField(unique=True, max_length=64)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bookings'


class City(models.Model):
    region = models.ForeignKey('Region', models.DO_NOTHING)
    name = models.CharField(max_length=150)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timezone = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Country(models.Model):
    iso_code = models.CharField(unique=True, max_length=8)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'country'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    star_rating = models.IntegerField(blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    main_phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    checkin_time = models.TimeField(blank=True, null=True)
    checkout_time = models.TimeField(blank=True, null=True)
    language_support = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel'


class Housekeeping(models.Model):
    room = models.ForeignKey('Room', models.DO_NOTHING, blank=True, null=True)
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    assigned_staff = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True)
    tasks = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'housekeeping'


class Inventory(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING)
    dt = models.DateField()
    available_count = models.IntegerField(blank=True, null=True)
    closed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory'
        unique_together = (('hotel', 'room_type', 'dt'),)


class InventoryLock(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING)
    dt = models.DateField()
    locked_by = models.CharField(max_length=128, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventory_lock'
        unique_together = (('hotel', 'room_type', 'dt'),)


class Invoice(models.Model):
    booking = models.ForeignKey(Bookings, models.DO_NOTHING)
    invoice_number = models.CharField(max_length=128, blank=True, null=True)
    pdf_url = models.CharField(max_length=1000, blank=True, null=True)
    issued_at = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class Notification(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    type = models.CharField(max_length=64, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    data = models.JSONField(blank=True, null=True)
    delivered = models.IntegerField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification'


class Photo(models.Model):
    entity_type = models.CharField(max_length=32)
    entity_id = models.IntegerField()
    url = models.CharField(max_length=1000)
    caption = models.CharField(max_length=255, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'photo'


class PushToken(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    token = models.CharField(max_length=500)
    platform = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'push_token'


class RatePlan(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    code = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    prepayment_required = models.IntegerField(blank=True, null=True)
    refundable = models.IntegerField(blank=True, null=True)
    cancellation_policy_id = models.CharField(max_length=255, blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rate_plan'


class Refund(models.Model):
    booking_payment = models.ForeignKey(BookingPayment, models.DO_NOTHING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'refund'


class Region(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'region'


class Review(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    rating = models.IntegerField()
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review'


class Room(models.Model):
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING)
    room_number = models.CharField(max_length=64, blank=True, null=True)
    floor = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room'


class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    code = models.CharField(max_length=64, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    max_adults = models.IntegerField(blank=True, null=True)
    max_children = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_type'


class SavedList(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    name = models.CharField(max_length=255, blank=True, null=True)
    list_type = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saved_list'


class SavedListItem(models.Model):
    saved_list = models.ForeignKey(SavedList, models.DO_NOTHING)
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    added_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'saved_list_item'


class SeoData(models.Model):
    entity_type = models.CharField(max_length=64, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seo_data'


class Setting(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'setting'


class ShiftAssignment(models.Model):
    shift_name = models.CharField(max_length=128, blank=True, null=True)
    staff_identifier = models.CharField(max_length=128, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shift_assignment'


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=200)
    uid = models.CharField(max_length=191)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.JSONField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=191)
    secret = models.CharField(max_length=191)
    key = models.CharField(max_length=191)
    provider_id = models.CharField(max_length=200)
    settings = models.JSONField()

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    socialapp = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING)
    site = models.ForeignKey(DjangoSite, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp', 'site'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount, models.DO_NOTHING)
    app = models.ForeignKey(SocialaccountSocialapp, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app', 'account'),)


class SupportComment(models.Model):
    ticket = models.ForeignKey('SupportTicket', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'support_comment'


class SupportTicket(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    subject = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'support_ticket'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=64, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    user_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Vendor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    contact_info = models.TextField(blank=True, null=True)
    contract_id = models.CharField(max_length=255, blank=True, null=True)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)
    contract_terms = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor'
