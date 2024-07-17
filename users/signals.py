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


# @receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('New user detected, 12122 creating user profile...')
    if created:
        try:
            user = instance
            Profile.objects.create(
                user = user,
                username = user.username,
                email = user.email,
                name = user.first_name)
        except Exception as e:
            print('something went wrong', e)

        # profile.save()
    print('Done!!')

# one way to use signals
post_save.connect(create_profile, sender=User)
# post_delete.connect(user_deleted, sender=Profile)
