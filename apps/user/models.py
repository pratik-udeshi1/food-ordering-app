from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from common.constants import Constants
from common.models import BaseModel


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Role(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{}-{}".format(self.id, self.name)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Role"
        ordering = ['-created_at']


class User(AbstractBaseUser, BaseModel):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=False, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    active_token = models.CharField(max_length=255, blank=True, null=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "{}----{}".format(self.email, self.id)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"
        ordering = ['-created_at']


class Session(BaseModel):
    device = (
        (Constants.WEB, Constants.WEB),
        (Constants.ANDROID, Constants.ANDROID),
        (Constants.IOS, Constants.IOS)
    )

    token = models.ForeignKey(OutstandingToken, on_delete=models.CASCADE, null=True)
    device_token = models.TextField(null=True)
    device_type = models.CharField(max_length=100, null=True, choices=device)
    is_safari = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(protocol="both", unpack_ipv4=False, blank=True, null=True)
    user = models.ForeignKey(User, related_name="session_set", on_delete=models.CASCADE, verbose_name="user")

    def __str__(self):
        return "{}".format(self.user)

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Session"
        ordering = ['-created_at']
