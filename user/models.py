from django.db import models
from django.contrib.auth.models import User

# Create your models here. 

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/beat/author/<filename>
    return 'profiles/{0}/{1}'.format(instance.user, filename)



class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(blank = True, null = True, verbose_name = "Profil Resmi", upload_to = user_directory_path)
    phone_number = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Tel No")
