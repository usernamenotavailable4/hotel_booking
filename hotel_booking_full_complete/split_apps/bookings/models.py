from django.db import models
import uuid
def gen_uuid(): return uuid.uuid4()

from users.models import User
from hotels.models import Hotel

class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=64, unique=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
