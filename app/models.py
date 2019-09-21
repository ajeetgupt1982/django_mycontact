from django.db import models
# the package required once need to validate the security and use if any relation like foreing key
from django.contrib.auth.models import User


class Contact(models.Model):
    # manage use once start the process of security base last use
    manager = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    info =  models.CharField(max_length=30)
    gender = models.CharField(max_length=30, choices=(
        ('male', 'Male'),
        ('female', 'Female')
    ))
    image = models.ImageField(upload_to='images/', blank=True)
    date_added = models.DateField(auto_now_add=True)

def __str__(self):
    return self.name

#ordering display the data

class Meta:
    ordering = ['-id']