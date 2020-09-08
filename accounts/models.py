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
    college  = models.ForeignKey('content.College', verbose_name="College", on_delete=models.CASCADE, blank=True, null=True)


    mobile = models.CharField(max_length=10,
                              validators=[RegexValidator(regex=r'[0-9]{10}', message='Invalid Mobile Number')],
                              blank=True)

    gender = models.CharField(max_length=1, choices=GENDERS, default='M')

    # registration_number = models.CharField('Registration number', max_length=7, unique=True,
    #                                        validators=[RegexValidator(regex=r'[a-zA-Z]{2}[0-9]{5}',
    #                                                                   message='Invalid Registration Number')])
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
        return reverse('accounts:index')

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


class TOTPVerification:

    def __init__(self):
        # secret key that will be used to generate a token,
        # User can provide a custom value to the key.
        self.key = random_hex(20)
        # counter with which last token was verified.
        # Next token must be generated at a higher counter value.
        self.last_verified_counter = -1
        # this value will return True, if a token has been successfully
        # verified.
        self.verified = False
        # number of digits in a token. Default is 6
        self.number_of_digits = 6
        # validity period of a token. Default is 30 second.
        self.token_validity_period = 35

    def totp_obj(self):
        # create a TOTP object
        totp = TOTP(key=self.key,
                    step=self.token_validity_period,
                    digits=self.number_of_digits)
        # the current time will be used to generate a counter
        totp.time = time.time()
        return totp

    def generate_token(self):
        # get the TOTP object and use that to create token
        totp = self.totp_obj()
        # token can be obtained with `totp.token()`
        token = str(totp.token()).zfill(6)
        return token

    def verify_token(self, token, tolerance=0):
        try:
            # convert the input token to integer
            token = int(token)
        except ValueError:
            # return False, if token could not be converted to an integer
            self.verified = False
        else:
            totp = self.totp_obj()
            # check if the current counter value is higher than the value of
            # last verified counter and check if entered token is correct by
            # calling totp.verify_token()
            if ((totp.t() > self.last_verified_counter) and
                    (totp.verify(token, tolerance=tolerance))):
                # if the condition is true, set the last verified counter value
                # to current counter value, and return True
                self.last_verified_counter = totp.t()
                self.verified = True
            else:
                # if the token entered was invalid or if the counter value
                # was less than last verified counter, then return False
                self.verified = False
        return self.verified


if __name__ == '__main__':
    # verify token the normal way
    phone1 = token_verification()
    generated_token = phone1.generate_token()
    print("Generated token is: ", generated_token)
    token = int(input("Enter token: "))
    print(phone1.verify_token(token))
    # verify token by passing along the token validity period.
    with mock.patch('time.time', return_value=1497657600):
        print("Current Time is: ", time.time())
        generated_token = phone1.generate_token()
        print(generated_token)
    with mock.patch(
        'time.time',
            return_value=1497657600 + phone1.token_validity_period):
        print("Checking time after the token validity period has passed."
              " Current Time is: ", time.time())
        token = int(input("Enter token: "))
        print(phone1.verify_token(token, tolerance=1))