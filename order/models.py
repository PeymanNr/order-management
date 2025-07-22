from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class TimeStampedModel(models.Model):
    """
     Abstract base model with created_at and updated_at fields.
     """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

class Order(TimeStampedModel):
    """
    Model representing an order created by a user.

    Attributes:
        product_name (str): Name of the product.
        quantity (int): Quantity ordered.
        price (Decimal): Total price.
        user (User): The user who placed the order.
    """

    product_name = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order by {self.user.username}: {self.product_name} x {self.quantity}"