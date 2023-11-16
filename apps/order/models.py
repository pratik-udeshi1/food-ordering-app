from django.db import models

from apps.menu.models import Menu
from apps.restaurant.models import Restaurant
from common.models import BaseModel


class Order(BaseModel):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'refunded'),
    )
    order_number = models.IntegerField(editable=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(Menu, through='OrderItem')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    final_total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-order_number').first()
            if last_order:
                self.order_number = last_order.order_number + 1
            else:
                self.order_number = 100  # Set initial order number

        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
