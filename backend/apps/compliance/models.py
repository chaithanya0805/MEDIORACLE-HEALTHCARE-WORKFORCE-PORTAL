from django.db import models
from apps.facilities.models import HealthcareRole, Facility
from apps.professionals.models import CredentialType
from django.conf import settings

class ComplianceRule(models.Model):
    role = models.ForeignKey(HealthcareRole, on_delete=models.CASCADE, related_name='compliance_rules')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True, blank=True, related_name='compliance_rules')
    credential_type = models.ForeignKey(CredentialType, on_delete=models.CASCADE)
    required = models.BooleanField(default=True)
    minimum_validity_days = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        facility_str = f" at {self.facility.name}" if self.facility else " (Global)"
        return f"{self.role.name} requires {self.credential_type.name}{facility_str}"

class ComplianceAudit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, default='OVERRIDE')
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE)
    shift = models.ForeignKey('shifts.Shift', on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} for {self.professional} on {self.timestamp}"
