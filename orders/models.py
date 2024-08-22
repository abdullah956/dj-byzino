from django.db import models
from django.conf import settings
from config.models import BasedModel


class Order(BasedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    products = models.JSONField() 
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_shipped = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, choices=[
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery'),
    ])
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('placed', 'Placed'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ])
    shipping_address = models.TextField()
    billing_address = models.TextField()
    phone = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Order {self.id} by {self.user.email}"
