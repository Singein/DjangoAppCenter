from django.contrib import admin

from DjangoAppCenter.packages.models import Package
from DjangoAppCenter.settings import load_settings_from_file

# Register your models here.
admin.site.register(Package)
admin.site.site_title = load_settings_from_file().get("ADMIN_SITE_TITLE", "DjangoAppCenter")
admin.site.site_header = load_settings_from_file().get("ADMIN_SITE_HEADER", "DjangoAppCenter")
