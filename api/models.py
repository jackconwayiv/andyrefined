import datetime

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    User,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class CreatedUpdated(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    nickname = models.CharField(max_length=200, blank=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Album(CreatedUpdated):

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    link_url = models.CharField(max_length=4000)
    thumbnail_url = models.CharField(max_length=4000)
    date = models.DateField(default=datetime.date.today, editable=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="albums", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Quote(models.Model):
    text = models.TextField()
    date = models.DateField(default=datetime.date.today, editable=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_quotes"
    )

    def __str__(self):
        return f"{self.text}"
