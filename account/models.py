from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "ADMIN")
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds a 'role' field to support admin and customer roles.
    """

    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(
        choices=Roles.choices, max_length=20, default=Roles.CUSTOMER
    )
    objects = CustomUserManager()

    def is_admin(self):
        """Check if user is an admin."""

        return self.role == self.Roles.ADMIN

    def is_customer(self):
        """Check if user is a customer."""

        return self.role == self.Roles.CUSTOMER

    def __str__(self):
        return f"{self.username} ({self.role})"
