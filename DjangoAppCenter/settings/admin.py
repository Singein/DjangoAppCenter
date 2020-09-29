from django.conf import settings
from django.contrib import admin

from DjangoAppCenter.settings.models import Settings

admin.AdminSite.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'DjangoAppCenter')
admin.AdminSite.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'DjangoAppCenter')
# Register your models here.
admin.site.register(Settings)
