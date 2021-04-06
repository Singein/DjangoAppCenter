import logging
from importlib import import_module

logger = logging.getLogger("PermissionInit")


class PermissionInitMixin:
    models_path: str = ""
    base_orm_models: tuple[str] = ("models.Model",)

    def ready(self):
        self.init_permissions()

    def init_permissions(self):
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Permission

        try:
            app_models = import_module(self.models_path)
        except ImportError:
            logger.error("Can't import module [%s]" % self.models_path)
            return

        for key, value in app_models.__dict__.items():
            if not isinstance(value, type):
                continue

            elif issubclass(value, [eval(m) for m in self.base_orm_models]):
                if hasattr(value, "_meta") and value._meta.abstract is True:
                    continue
                if not ContentType.objects.filter(app_label=self.name).filter(model=key.lower()).exists():
                    ContentType.objects.create(app_label=value._meta.app_label, model=key.lower())

            else:
                continue

        content_types = ContentType.objects.filter(app_label=self.name)
        for q in content_types:
            permissions = [p["codename"] for p in Permission.objects.filter(content_type_id=q.id).values("codename")]
            for perm in ["add_%s" % q.model, "change_%s" % q.model, "view_%s" % q.model, "delete_%s" % q.model]:

                if perm not in permissions:
                    Permission.objects.create(name="can %s" % perm.replace("_", " "), content_type=q,
                                              codename=perm)
