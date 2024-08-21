from django.db import models
from config.models import BasedModel
from django.conf import settings
from categories.models import Product 

class Cart(BasedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
    def __str__(self):
        return f"{self.product.name}x{self.quantity} in {self.user.email}'s cart"
