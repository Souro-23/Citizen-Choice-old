from django.db import models

from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField()
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)