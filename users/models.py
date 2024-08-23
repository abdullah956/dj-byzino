from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator
from config.models import BasedModel
from .managers import UserManager
from django.db.models.signals import post_delete ,  pre_save
from django.dispatch import receiver


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
    
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

@receiver(post_delete, sender=User)
def delete_image_file(sender, instance, **kwargs):
    instance.avatar.delete(False)

@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_avatar = sender.objects.get(pk=instance.pk).avatar
    except sender.DoesNotExist:
        return False

    new_avatar = instance.avatar
    if not old_avatar == new_avatar:
        if old_avatar:
            old_avatar.delete(False)


class Subscriber(BasedModel):
    email = models.EmailField(unique=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.email} - {'Subscribed' if self.is_subscribed else 'Not Subscribed'}"
    
class ContactMessage(BasedModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.email}"
