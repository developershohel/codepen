import unicodedata
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, is_password_usable
from django.db import models
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from codepen.functions import password_helper_text
from django.contrib.auth import password_validation


# Create your models here.
class userAdminManager(BaseUserManager):
    def create_user(self, username, email, password, first_name, last_name, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Your account is not verified')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Super User account is not verified')
        return self.create_user(username, email, password, first_name, last_name, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator
    password_validator = CommonPasswordValidator
    username = models.CharField(max_length=100, null=False, blank=False, unique=True, validators=[username_validator],
                                help_text=_(
                                    "Required. 150 characters or fewer. Letters, digits and _ only."
                                ))
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False,
                                help_text=password_helper_text())
    first_name = models.CharField(max_length=100, null=False, blank=False, help_text=_(
        "Required. 150 characters or fewer. Letters, digits and whitespace only."
    ))
    last_name = models.CharField(max_length=100, null=False, blank=False, help_text=_(
        "Required. 150 characters or fewer. Letters, digits and whitespace only."
    ))
    follower = models.ManyToManyField('self', blank=True)
    following = models.ManyToManyField('self', blank=True)
    user_blocked = models.ManyToManyField('self', blank=True)
    user_type = models.IntegerField(null=False, blank=False, default=0)
    user_trail = models.BooleanField(null=True, blank=True, default=False)
    user_status = models.BooleanField(null=True, blank=True, default=False)
    user_activation_key = models.CharField(max_length=255,  blank=False, null=False)
    user_verification_code = models.IntegerField(blank=False, null=False, default=0)
    user_registered = models.DateTimeField(auto_now_add=True)
    user_modified = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = userAdminManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username} {self.email} {self.first_name} {self.last_name}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return self.get_username()

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.password,
            algorithm="sha256",
        ).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return "email"

    @classmethod
    def normalize_username(cls, username):
        return (
            unicodedata.normalize("NFKC", username)
            if isinstance(username, str)
            else username
        )


class UserLogs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    user_country = models.CharField(max_length=100, blank=True, null=True)
    user_city = models.CharField(max_length=100, blank=True, null=True)
    user_ip = models.CharField(max_length=100, blank=True, null=True)
    user_login = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f'{self.id} {self.user.username} {self.user_country} {self.user_ip} {self.user_login}'
