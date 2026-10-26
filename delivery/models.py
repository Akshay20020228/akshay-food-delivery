from django.db import models

# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
    ]
    status = models.CharField(
    max_length=30,
    choices=STATUS_CHOICES,
    default="Pending"
)


    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

