from apps.payment import models as payment_model
from django.contrib import admin

# Register your models here.
admin.site.register(payment_model.PaymentMethod)
