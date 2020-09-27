import logging
import os
import threading

from django.db import models

from DjangoAppCenter.extensions.fields.snowflake import SnowFlakeField

logger = logging.getLogger("admin")


# Create your models here.

def install(repository, name, version, pip_version):
    os.system(f"{pip_version} install -i {repository} {name}=={version}")
    self.installing = False
    self.old_version = version
    super(Package, self).save()
    logger.info(f"Package {name} {version} install task finished.")


class Package(models.Model):
    id = SnowFlakeField(primary_key=True)
    name = models.CharField(verbose_name="package name",max_length=255)
    repository = models.CharField(verbose_name="repository",max_length=255, default="https://pypi.org/simple")
    enable = models.BooleanField(verbose_name="enable", default=True)
    version = models.CharField(verbose_name="version", max_length=255, default="0.0.1")
    old_version = models.CharField(verbose_name="old_version", max_length=255, default="0.0.1", editable=False)
    is_app = models.BooleanField(help_text="register the package as an django app", default=False)
    installing = models.BooleanField(default=False)
    pip_version = models.CharField(verbose_name="pip version",max_length=255, choices=(("pip3", "pip3"), ("pip", "pip")),
                                   default="pip")

    def __str__(self):
        return f"{self.name} v{self.version}"

    def install(self):
        os.system(f"{self.pip_version} install -i {self.repository} {self.name}=={self.version}")
        # self.installing = False
        # self.old_version = self.version
        # super(Package, self).save()
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
