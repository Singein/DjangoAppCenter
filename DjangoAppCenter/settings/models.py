from django.db import models


# Create your models here.

class Settings(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255)
    value = models.TextField()
    addition = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.key
