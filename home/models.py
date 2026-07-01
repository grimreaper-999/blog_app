from django.db import models
from django.conf import settings



# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    bio= models.TextField(max_length=300 ,null=True ,default=True)

    def __str__(self):
        return f"profile for {self.user.username}"