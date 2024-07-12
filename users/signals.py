from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete 

#signals receiver for post_save
@receiver(post_save, sender=Profile)   
def profile_updated(sender, instance, created, **kwargs):
    print('User Updated!!')
    print('Created?', created)
    print('instance', instance)


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    print('Deleting user...')
    user = instance.user 
    user.delete()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('New user detected, creating user profile...')
    user = instance
    profile = Profile.objects.create(
        user = user,
        username = user.username,
        email = user.email,
        name = user.first_name,
    )

    print('Done!!')

# one way to use signals
# post_save.connect(profile_updated, sender=Profile)
# post_delete.connect(user_deleted, sender=Profile)
