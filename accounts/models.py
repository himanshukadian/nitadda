from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.password_validation import validate_password

from django_otp.oath import TOTP
from django_otp.util import random_hex
from unittest import mock
import time

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=username + '',
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDERS = (('M', 'Male'), ('F', 'Female'))

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.ForeignKey('content.College', verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)
    mobile = models.CharField(max_length=10,
                              validators=[RegexValidator(regex=r'[0-9]{10}', message='Invalid Mobile Number')],
                              blank=True)

    gender = models.CharField(max_length=1, choices=GENDERS, default='M')

    admin = models.CharField(max_length=1, default='N')
    password = models.CharField('password', max_length=128, validators=[validate_password])
    is_active = models.BooleanField(default=False, verbose_name='Active',
                                    help_text='Designates whether this user should be treated as active. '
                                              'Unselect this instead of deleting accounts.')
    is_admin = models.BooleanField(default=False, verbose_name='Staff status',
                                   help_text='Designates whether the user can log into this admin site.')
    image = models.ImageField(default='download.jpg', upload_to='profile/')
    notifications = models.IntegerField(default=0)
    noti_messages = models.CharField(max_length=500, blank=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('accounts:profile')

class ContactUsMessage(models.Model) :

    sender_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10,
                              validators=[RegexValidator(regex=r'[0-9]{10}', message='Invalid Mobile Number')],
                              blank=True)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return self.id

