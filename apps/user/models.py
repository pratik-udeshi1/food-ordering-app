from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
#
# from common import model_utils
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from common.constants import Constants
from common.models import BaseModel
# from common.constants import Constants, ApplicationMessages
#
# from rest_framework.exceptions import ValidationError
# from rest_framework import status
from rest_framework.response import Response


class MyUserManager(BaseUserManager):
    """The Custom BaseManager Class"""

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


#
#
class Role(BaseModel):
    """
    Role model is to specify an id and name to the roles of users
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        String representation
        :return:
        """
        return "{}-{}".format(self.id, self.name)

    class Meta:
        """
        Verbose name and verbose plural
        """
        verbose_name = "Role"
        verbose_name_plural = "Role"
        ordering = ['-created_at']


class User(AbstractBaseUser, BaseModel):
    """
    User model with email and password as a login credentials
    """

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

    def __str__(self):
        """
        String representation of name
        :return:
        """
        return "{}-{}".format(self.email, self.id)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # All admins are staff
        return self.is_admin

    class Meta:
        """
        Verbose name and verbose plural
        """
        verbose_name = "User"
        verbose_name_plural = "User"
        ordering = ['-created_at']

    def tokens(self):
        """
        For retrieving tokens from simple-jwt
        """
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


#
#     @staticmethod
#     def update_password(user_id, new_password, old_password=None):
#         """
#         For updating the existing password of a user
#         """
#         try:
#             obj = User.objects.get(id=user_id)
#             if obj.password == model_utils.make_password(old_password):
#                 obj.password = model_utils.make_password(new_password)
#                 obj.save()
#                 return Response(str(ApplicationMessages.PASSWORD_CHANGE),
#                                 status=status.HTTP_200_OK)
#             else:
#                 raise ValidationError(ApplicationMessages.CURRENT_PASSWORD_INCORRECT,
#                                       status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             raise ValidationError(ApplicationMessages.USER_NOT_EXISTS,
#                                   status.HTTP_400_BAD_REQUEST)
#
#
class Session(BaseModel):
    """Session table store data with session id"""

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
        """
        String representation of session
        :return:
        """
        return "{}".format(self.user)

    class Meta:
        """
        Verbose name and verbose name plural
        """
        verbose_name = "Session"
        verbose_name_plural = "Session"
        ordering = ['-created_at']


class VerificationToken(BaseModel):
    """
    1. Save password reset verification token
    2. Save user verification token
    On the basis of token type
    """
    PASSWORD_RESET = 'PASSWORD_RESET'
    VERIFICATION = 'VERIFICATION'
    INVITATION = 'INVITATION'

    TYPES = (
        (PASSWORD_RESET, 'Password Reset'),
        (VERIFICATION, 'Account Verification'),
        (INVITATION, 'Examiner Invitation'),
    )
    user = models.ForeignKey(User, related_name="verification_token", on_delete=models.CASCADE)
    token_type = models.CharField(max_length=100, blank=False, null=False, choices=TYPES)
    token = models.CharField(max_length=255, blank=False, null=False)
    expiry_time = models.DateTimeField(null=True, blank=True)
    token_used = models.BooleanField(default=False)

    def __str__(self):
        """
        String  representation of token
        :return:
        """
        return "{}-{}-{}-{}".format(self.user.email, self.token, self.token_type, self.token_used)

    class Meta:
        """
        Verbose name and verbose name plural
        """
        verbose_name = "VerificationToken"
        verbose_name_plural = "VerificationToken"
        ordering = ['-created_at']

    @staticmethod
    def create_password_token(kwargs):
        """
        Creates a Token and return user obj
        """

        obj = VerificationToken(**kwargs)
        obj.token_type = Constants.RESET_PASSWORD_TOKEN
        obj.save()
        return obj
