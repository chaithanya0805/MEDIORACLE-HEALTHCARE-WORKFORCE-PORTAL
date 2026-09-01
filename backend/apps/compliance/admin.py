from django.contrib import admin
from apps.compliance.models import ComplianceRule, ComplianceAudit

admin.site.register(ComplianceRule)
admin.site.register(ComplianceAudit)
