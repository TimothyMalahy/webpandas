from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, valid_extensions
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class DataFrame(models.Model):
    """
    This holds the model for dataframe
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, help_text='Name of the file ')
    dataframe = models.FileField(upload_to='core/', help_text=valid_extensions() ,validators=[validate_file_extension])
    


    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()