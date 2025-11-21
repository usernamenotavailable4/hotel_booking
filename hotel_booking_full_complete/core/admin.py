from django.contrib import admin
from .models import *
models = [m for m in globals().values() if hasattr(m, '__name__') and getattr(m, '__module__','').startswith('core.models')]
# Register models safely
for name, obj in list(globals().items()):
    if hasattr(obj, '__name__') and getattr(obj, '__module__','').startswith('core.models'):
        try:
            admin.site.register(obj)
        except Exception:
            pass
