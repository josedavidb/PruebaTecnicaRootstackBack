from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Create your models here.

class Profile(models.Model):
    '''
    Represent a user's profile (extended). 
    There is always a single Profile instance for each User instance, 
    and they are automatically created and deleted at the same time.
    '''
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER,'O')
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    zip_code = models.IntegerField()
    picture = models.ImageField()
    birthdate = models.DateField()
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='M')

    def __str__(self):
    	return str(self.user)

# Triggers for Profile Model

@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, **kwargs):
    '''
    Create the profile associated with a user right after the user has been created.
    '''
    
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    '''
    Save the user profile associated with a User right after the user is saved,
     after any change.
    '''
    instance.profile.save()

@receiver(post_delete, sender=Profile)
def delete_associated_entities_to_profile(sender, instance, **kwargs):
    '''
    Trigger to take charge of any entity associated 
    with Profile after its elimination.
    '''
    pass 

class Grill(models.Model):

    '''
    Represent a Grill object
    '''
    model = models.CharField(max_length=20)
    description = models.CharField(max_length=80)
    zip_code = models.IntegerField()
    width = models.FloatField()
    height = models.FloatField()
    weight = models.FloatField()
    color = models.CharField(max_length=15,blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class GrillImage(models.Model):

    '''
	Represent a image asociated to a event
	'''

    grill = models.ForeignKey(Grill, on_delete=models.CASCADE)
    image = models.ImageField()