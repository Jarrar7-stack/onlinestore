from django.db import models
from django.contrib.auth.models import User  


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links item to a specific user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Links item to a specific product
    quantity = models.PositiveIntegerField(default=1)  # Ensures quantity is always positive
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def save(self, *args, **kwargs):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if self.product.stock < self.quantity:
            raise ValueError("Not enough stock available.")
        super().save(*args, **kwargs)