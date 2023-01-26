from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/beat/author/<filename>
    return 'profiles/{0}/{1}'.format(instance.user, filename)

USER_TYPES = (("Usta", "usta"), ("Yönetici", "yonetici"), ("Müşteri", "musteri"), ("Cari", "cari"))

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_type = models.CharField(choices = USER_TYPES, default = "usta", max_length = 30)
    image = models.ImageField(blank = True, null = True, verbose_name = "Profil Resmi", upload_to = user_directory_path)
    phone_number = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Tel No")
    