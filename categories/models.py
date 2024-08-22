from django.db import models
from config import settings
from config.models import BasedModel

class Category(BasedModel):
    name = models.CharField(max_length=255) 
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name


class Product(BasedModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_on_sale = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.category.name}'


class Review(BasedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    review = models.TextField()
    stars = models.PositiveIntegerField()
    def __str__(self):
        return f"Review by {self.user.email} on {self.product.name}"