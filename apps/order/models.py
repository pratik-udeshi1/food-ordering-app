from django.db import models

from apps.inventory.models import InventoryItem


class Order(models.Model):
    items = models.ManyToManyField(InventoryItem, through='OrderItem')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
