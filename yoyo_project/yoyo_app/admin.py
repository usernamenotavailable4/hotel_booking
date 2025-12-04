from django.contrib import admin
from django.apps import apps

# Automatically register all models in the yoyo_app application.
app_models = apps.get_app_config('yoyo_app').get_models()

for model in app_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # Model already registered; ignore.
        pass
