from django.db import models
from django.contrib.auth.models import User
import uuid
# for signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class  Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
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
    
    class Meta:
        ordering = ['created_date_time']
            

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


class Message(models.Model):
    '''on delete keep messages but set sender to null
    sender may not have profile, but will have to add name, email
    blank=true form can be submitted without a sender
    related_name is going to connect profile to messages,
    '''
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='messages')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True,
                          editable=False)
    
    def __str__(self) -> str:
        return self.subject
    
    class Meta:
        # order by unread messages, and then message time
        ordering = ['is_read', '-created_date_time' ]
 
