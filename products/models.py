from django.db import models
from django.contrib.auth.models import User  


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_new = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Product, through='OrderItem') 
    def calculate_total_price(self):
        order_items = self.orderitem_set.all()  
        self.total_price = sum(item.product.price * item.quantity for item in order_items)
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"




class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)  
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def calculate_cart_total(user):
        cart_items = CartItem.objects.filter(user=user)
        total = sum(item.quantity * item.product.price for item in cart_items)
        return total


    def save(self, *args, **kwargs):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if self.product.stock < self.quantity:
            raise ValueError("Not enough stock available.")
        super().save(*args, **kwargs)