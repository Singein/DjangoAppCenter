from django.conf import settings
from django.contrib import admin
from django.db import models

from DjangoAppCenter.extensions.fields.django_monaco_editor.widgets import AdminMonacoEditorWidget
from DjangoAppCenter.settings.models import Settings

admin.AdminSite.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'DjangoAppCenter')
admin.AdminSite.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'DjangoAppCenter')


# Register your models here.


class SettingsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMonacoEditorWidget}
    }
    ordering = ["key"]
    search_fields = ["key", "name"]
    list_display = ["name", "key"]


admin.site.register(Settings, SettingsAdmin)
