from django.db import models
from django.contrib.auth.models import User

# Create your models here. 

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/beat/author/<filename>
    return 'profiles/{0}/{1}'.format(instance.user, filename)

class UserCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Kullanıcı Kategorisi")
    
    class Meta:   
        verbose_name_plural = "user categories"

    def __str__(self):
        return self.title
    
class StaffCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name = "Personel Kategorisi")
    
    class Meta:   
        verbose_name_plural = "staff categories"

    def __str__(self):
        return self.title

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_category = models.ForeignKey(UserCategory, on_delete = models.SET_DEFAULT, default = 2, verbose_name = "Kullanıcı Kategorisi")
    staff_category = models.ForeignKey(StaffCategory, blank = True, null = True, on_delete = models.SET_DEFAULT, default = 1, verbose_name = "Personel Kategorisi")
    image = models.ImageField(blank = True, null = True, verbose_name = "Profil Resmi", upload_to = user_directory_path)
    phone_number = models.CharField(max_length = 200, blank = True, null = True, verbose_name = "Tel No")
