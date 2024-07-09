import logging
import os
import threading

from django.db import models

from DjangoAppCenter.settings.models import NameSpace

logger = logging.getLogger("admin")


# Create your models here.

class PackageRepository(models.Model):
    name = models.CharField(verbose_name="repository name", max_length=255)
    url = models.CharField(verbose_name="repository url", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "package_repository"


class Package(models.Model):
    name = models.CharField(verbose_name="package name", max_length=255)
    app_name = models.CharField(verbose_name="app name", max_length=255)
    repository = models.ForeignKey(to=PackageRepository, verbose_name="repository", max_length=255,
                                   on_delete=models.CASCADE)
    enable = models.BooleanField(verbose_name="enable", default=True)
    version = models.CharField(verbose_name="version", max_length=255, default="0.0.1")
    old_version = models.CharField(verbose_name="old_version", max_length=255, default="0.0.1", editable=False)
    register_as_django_app = models.BooleanField(help_text="register the package as an django app", default=False)
    installing = models.BooleanField(default=False, editable=False, verbose_name="installing")
    pip_version = models.CharField(verbose_name="pip version", max_length=255,
                                   choices=(("pip3", "pip3"), ("pip", "pip")),
                                   default="pip")
    setting_namespace = models.ForeignKey(to=NameSpace, verbose_name="settings namespace for app", blank=True,
                                          null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} v{self.version}"

    def install(self):
        os.system(f"{self.pip_version} install -i {self.repository} {self.name}=={self.version}")
        self.installing = False
        self.old_version = self.version
        super(Package, self).save()
        logger.info(f"Package {self.name} {self.version} install task finished.")

    def save(self):
        super().save()
        if self.installing:
            logger.info(f"Package {self.name} haven't finished last installing task.")
            return

        if self.version == self.old_version:
            return

        # install the new version
        self.installing = True
        super(Package, self).save()

        logger.info(f"Package {self.name} v{self.version} start installing.")
        task = threading.Thread(target=self.install)
        task.start()

    class Meta:
        db_table = "package"
