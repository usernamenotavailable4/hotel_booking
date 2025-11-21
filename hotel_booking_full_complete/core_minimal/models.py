from django.db import models
import uuid

def gen_uuid(): return uuid.uuid4()

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=32, default='published')

class RoomType(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)
    name = models.CharField(max_length=255)

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=64, unique=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
