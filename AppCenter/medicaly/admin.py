from django.contrib import admin

# Register your models here.

from AppCenter.medicaly.models import BodyPart, OrganSystem, Symptom, Disease, SymptomToDisease


for model in BodyPart, OrganSystem, Symptom, Disease, SymptomToDisease:

    admin.site.register(model)
