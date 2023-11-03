from django.contrib import admin
from apps.user import models as user_model

# Register your models here.
admin.site.register(user_model.User)
