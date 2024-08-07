import logging
import os
import threading

from django.db import models

from DjangoAppCenter.settings.loader import merge_profile

logger = logging.getLogger("application-models")


# Create your models here.
class Application(models.Model):
    """
    应用描述
    """
    name = models.CharField(verbose_name="app module name", max_length=255, unique=True)
    enabled = models.BooleanField(verbose_name="enable", default=False)
    order = models.IntegerField(verbose_name="order in installed apps", default=0)
    description = models.TextField(verbose_name="description", blank=True, null=True)
    router = models.CharField(verbose_name="router", max_length=1024, blank=True, null=True)
    settings = models.TextField(verbose_name="django settings", max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at", editable=False)

    def __str__(self):
        return f'{self.name}'

    def enable(self):
        # 判断当前的依赖对应的包是否都已经安装了
        requirements = [{"name": r.name, "version": r.version} for r in self.requirements.all()]
        # Package.objects.filter(name__in=[r.name for r in packages]).update(version=r.version for r in packages)
        for requirement in requirements:
            package = Package.objects.filter(name=requirement["name"]).first()
            if package is None:
                # 安装依赖包
                package = Package.objects.create(name=requirement["name"], version=requirement["version"])
                package.install()
            else:
                if package.version != requirement["version"]:
                    package.update(version=requirement["version"])
                else:
                    logger.info(f"Package {package.name} v{package.version} is already installed.")

    class Meta:
        ordering = ["-id"]
        verbose_name = "application"
        verbose_name_plural = "applications"
        db_table = "dac_applications"


class Requirement(models.Model):
    """
    应用依赖
    """
    name = models.CharField(verbose_name="package name", max_length=255)
    version = models.CharField(verbose_name="version", max_length=255, default="0.0.1")
    application = models.ForeignKey(Application, db_constraint=False, on_delete=models.CASCADE,
                                    related_name="requirements")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at", editable=False)

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ["application_id"]
        unique_together = ("name", "application")
        verbose_name = "requirement"
        verbose_name_plural = "requirements"
        db_table = "dac_requirements"


class Package(models.Model):
    name = models.CharField(verbose_name="package name", max_length=255)
    version = models.CharField(verbose_name="version", max_length=255, default="", blank=True)
    rollback_version = models.CharField(verbose_name="rollback_version", max_length=255, default="",
                                        editable=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at", editable=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated at", editable=False)

    def __str__(self):
        return f"{self.name} v{self.version}"

    def install(self):
        try:
            # 读取优先级最小的repository
            repository = PypiRepository.objects.all().order_by("priority").first()
            os.system(f"pip install -i {repository.url} {self.name}=={self.version}")
            logger.info(f"Package {self.name} {self.version} install task finished.")
        except Exception as e:
            logger.error(f"Package {self.name} {self.version} install task failed. {e}")

    def update(self, version: str):
        """
        更新包
        :param version:
        :return:
        """
        if self.version == version:
            return

        self.rollback_version = self.version
        self.version = version
        self.save()
        self.install()

    def save(self):
        super().save()
        if self.installing:
            logger.info(f"Package {self.name} haven't finished last installing task.")
            return

        if self.version == self.old_version:
            merge_profile(self.app_name, self.settings)
            return

        # install the new version
        self.installing = True
        super(Package, self).save()

        logger.info(f"Package {self.name} v{self.version} start installing.")
        task = threading.Thread(target=self.install)
        task.start()

    class Meta:
        ordering = ["-id"]
        unique_together = ("name", "version")
        verbose_name = "package"
        verbose_name_plural = "packages"
        db_table = "dac_packages"


class PypiRepository(models.Model):
    """
    pypi repository
    """
    name = models.CharField(verbose_name="repository name", max_length=255)
    url = models.CharField(verbose_name="repository url", max_length=255)
    # 优先级， 值越小越优先使用
    priority = models.IntegerField(verbose_name="priority", default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["priority"]
        verbose_name = "pypi repository"
        verbose_name_plural = "pypi repositories"
        db_table = "dac_pypi_repositories"
