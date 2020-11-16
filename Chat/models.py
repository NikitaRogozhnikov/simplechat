from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

#from Chat.managers import PersonManager

# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(User)

    def get_absolute_url(self):
        return '/chat/%i'% self.pk

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    messages = models.TextField()
 
 
    def __str__(self):
        return self.messages

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    banned=models.BooleanField(default=False)
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
'''