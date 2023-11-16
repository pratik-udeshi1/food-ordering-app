from django.contrib import admin

from apps.restaurant import models as restaurant_model

# Register your models here.
admin.site.register(restaurant_model.Restaurant)
