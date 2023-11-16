from django.db import models

from common.models import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name
