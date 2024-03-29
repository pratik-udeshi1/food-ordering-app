from django.db import models

from common.models import BaseModel


class Restaurant(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}----{}".format(self.name[:15], self.id)
