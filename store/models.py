from django.db import models
from django.contrib.auth.models import User


class Shoe(models.Model):
    CATEGORY_CHOICES = [
        ('men', "Men's"),
        ('women', "Women's"),
    ]

    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='shoes/')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='men')  # 👈 Add this line

    def __str__(self):
        return self.name


    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.shoe.name} x {self.quantity} - {self.user.username}"



class Order(models.Model):
    PAYMENT_CHOICES = [
        ('before', 'Pay Before Delivery'),
        ('after', 'Pay After Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(default="example@gmail.com")
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.shoe.name}"

    def total_price(self):
        return self.quantity * self.shoe.price
