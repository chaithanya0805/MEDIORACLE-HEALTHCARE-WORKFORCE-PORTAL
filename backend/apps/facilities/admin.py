from django.contrib import admin
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty, Skill, StaffingRequirement

admin.site.register(Facility)
admin.site.register(Department)
admin.site.register(Ward)
admin.site.register(HealthcareRole)
admin.site.register(Specialty)
admin.site.register(Skill)
admin.site.register(StaffingRequirement)
