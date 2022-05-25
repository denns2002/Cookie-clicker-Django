from django.contrib import admin

# Register your models here.
from .models import \
    Boost, \
    Core

admin.site.register(Boost)
admin.site.register(Core)