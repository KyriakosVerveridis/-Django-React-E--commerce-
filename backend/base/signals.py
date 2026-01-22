from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(pre_save, sender=User)
def updateUser(sender, instance, **kwargs):
    """
    Signal receiver that automatically sets the username to the user's email 
    before the User instance is saved to the database.
    """
    user = instance
    if user.email != "":
        user.username = user.email # Synchronize username with email address
