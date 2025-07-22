from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

class Order(TimeStampedModel):
    product_name = models.CharField(max_length=64)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order by {self.user.username}: {self.product_name} x {self.quantity}"