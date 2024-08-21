from django.db import models
from config.models import BasedModel

class Category(BasedModel):
    name = models.CharField(max_length=255) 
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name
