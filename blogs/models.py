from django.db import models
from config.models import BasedModel
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Blog(BasedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    picture = models.ImageField(upload_to='blog_pictures/')

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.picture.delete(save=False)
        super().delete(*args, **kwargs)

@receiver(post_delete, sender=Blog)
def delete_image_file(sender, instance, **kwargs):
    if instance.picture:
        instance.picture.delete(False)
