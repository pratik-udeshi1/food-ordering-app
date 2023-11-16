from django.contrib import admin

from apps.order import models as order_model

# Register your models here.
admin.site.register(order_model.Order)
admin.site.register(order_model.OrderItem)
