from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        CUSTOMER = "customer", "Customer"

    role = models.CharField(choices=Roles.choices, max_length=20,
                            default=Roles.CUSTOMER)

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def is_customer(self):
        return self.role == self.Roles.CUSTOMER