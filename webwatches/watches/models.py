from django.db import models
from django.contrib.auth.models import User

class Watch(models.Model):
    name = models.CharField(max_length=100)
    brand = models.TextField(max_length=30)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='watches/')
    created_at = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.watch.name} - {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Watch)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Order {self.id} - {self.status}"
