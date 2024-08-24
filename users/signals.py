from .models import Profile
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete 
from django.core.mail import send_mail
from django.conf import settings

#signals receiver for profile post_save
@receiver(post_save, sender=Profile)   
def profile_updated(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# singal for deleting user account when profile is deleted
@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    user = instance.user 
    user.delete()


# signal for creating a profile when User is created. 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            user = instance
            profile = Profile.objects.create(
                user = user,
                username = user.username,
                email = user.email,
                name = user.first_name)
        except Exception as e:
            print('something went wrong', e)

        # send welcome message 
        send_mail(
            "Welcome to developers hub",
            "Hello, good to have you here",
            settings.EMAIL_HOST_USER, 
            [profile.email], fail_silently=False)
        # profile.save()
    print('Done!!')

# one way to use signals
# post_save.connect(create_profile, sender=User)
# post_delete.connect(user_deleted, sender=Profile)
