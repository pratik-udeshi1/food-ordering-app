from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from apps.restaurant.models import Restaurant
from common.models import BaseModel


class MenuImageStorage(S3Boto3Storage):
    location = 'local-testing-1'  # S3 bucket sub folder where images will be stored
    file_overwrite = False  # Prevent overwriting existing files with the same name


class Menu(BaseModel):
    CLASSIFICATION_CHOICES = (
        ('neither', 'Neither'),
        ('vegan', 'Vegan'),
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=50)
    classification = models.CharField(max_length=10, choices=CLASSIFICATION_CHOICES, default=0)
    image = models.ImageField(upload_to='menu', storage=MenuImageStorage, null=True, blank=True)

    spicy = models.BooleanField(default=False)
    contains_peanuts = models.BooleanField(default=True)
    gluten_free = models.BooleanField(default=False)
    availability = models.BooleanField(default=True)
    calories = models.CharField(max_length=10, default=0)

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menu items'
        ordering = ['category', 'name']

    def __str__(self):
        return "{}----{}".format(self.name[:15], self.id)
