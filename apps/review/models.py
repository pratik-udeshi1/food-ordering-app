from django.db import models

from apps.user.models import User
from common.models import BaseModel


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
