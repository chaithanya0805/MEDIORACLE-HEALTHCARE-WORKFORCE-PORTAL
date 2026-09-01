from django.contrib import admin
from apps.professionals.models import (
    ProfessionalProfile, Qualification, WorkHistory, ProfessionalSkill,
    ProfessionalAvailability, ProfessionalPreference, ProfessionalInsurance,
    ProfessionalDocument, CredentialType, Credential
)

admin.site.register(ProfessionalProfile)
admin.site.register(Qualification)
admin.site.register(WorkHistory)
admin.site.register(ProfessionalSkill)
admin.site.register(ProfessionalAvailability)
admin.site.register(ProfessionalPreference)
admin.site.register(ProfessionalInsurance)
admin.site.register(ProfessionalDocument)
admin.site.register(CredentialType)
admin.site.register(Credential)
