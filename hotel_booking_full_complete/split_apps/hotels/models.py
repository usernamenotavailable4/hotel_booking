from django.db import models
import uuid
def gen_uuid(): return uuid.uuid4()

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
