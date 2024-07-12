from django.db import models
from django.contrib.auth.models import User
import uuid
# for signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class  Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, 
                                      default='profiles/default_prof_pic.png', upload_to='profiles/') 
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    created_date_time = models.TimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, unique=True)
    
    def __str__(self) -> str:
        return str(self.username) 
    

class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, 
                            editable=False,  unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE,
                              blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)
    created_date_time = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)

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

 
