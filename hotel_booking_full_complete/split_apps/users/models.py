from django.db import models
import uuid
def gen_uuid(): return uuid.uuid4()

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=gen_uuid, editable=False)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
