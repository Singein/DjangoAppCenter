from django.conf import settings
from django.contrib import admin

from DjangoAppCenter.settings.models import Settings

admin.AdminSite.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'DjangoAppCenter')
admin.AdminSite.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'DjangoAppCenter')


# Register your models here.


class SettingsAdmin(admin.ModelAdmin):
    ordering = ["key"]
    search_fields = ["key", "name"]
    list_display = ["key", "name"]


admin.site.register(Settings, SettingsAdmin)
