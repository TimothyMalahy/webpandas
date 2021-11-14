from django.db import models
from django.contrib.auth.models import User
from .validators import validate_file_extension, valid_extensions

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