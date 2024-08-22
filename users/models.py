from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from config import settings
from config.models import BasedModel
from .managers import UserManager


class User(AbstractUser, BasedModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"