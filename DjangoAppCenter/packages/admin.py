from django.contrib import admin

from DjangoAppCenter.packages.models import Package
from DjangoAppCenter.settings.storage import django_app_center_settings

# Register your models here.
admin.site.register(Package)
admin.site.site_title = django_app_center_settings.get("ADMIN_SITE_TITLE", "DjangoAppCenter")
admin.site.site_header = django_app_center_settings.get("ADMIN_SITE_HEADER", "DjangoAppCenter")
