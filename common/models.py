import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Base Model class to add a id, created_at and updated_at field as common for all models.
    properties: id (uuid), created_at, updated_at (timestamp)
    """

    class Meta:
        """
        abstract base model class.
        abstract = True (abstract base class),
        ordering = ['field'],
        db_table = 'custom_db_table'
        Note: Django does make one adjustment to the Meta class of an abstract base class: before installing the Meta attribute, it sets abstract=False.
        """

        abstract = True

    objects = models.Manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """
        print: {id}/created_date
        :return:
        """
        return "{}-{}".format(self.id, self.created_at)


class Permission(models.Model):
    """
    Permission model has an id and permission. It can store id with the permission and these id can be used to map
    roles with permissions
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permission = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        """
        print: {id}/permission
        :return:
        """
        return "{}".format(self.permission)
