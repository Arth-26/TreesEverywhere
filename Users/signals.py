from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        created_profile = Profile.objects.create()
        instance.profile = created_profile
        instance.save()

@receiver(post_delete, sender=CustomUser)
def delete_profile(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.delete()
