from django.contrib import admin

from apps.menu import models as menu_model

admin.site.register(menu_model.Menu)
