from django.db import models


# Create your models here.

class Settings(models.Model):
    name = models.CharField(verbose_name="设置名称", max_length=255, null=True, blank=True)
    addition = models.CharField(verbose_name="备注说明", null=True, blank=True, max_length=255)
    key = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return self.key

    class Meta:
        db_table = "dac_settings"
