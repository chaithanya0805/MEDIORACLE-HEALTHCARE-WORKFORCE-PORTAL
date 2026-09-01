from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class AuditEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100) # LOGIN, SHIFT_CREATE, TIMESHEET_APPROVE, etc.
    object_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    previous_data = models.JSONField(null=True, blank=True)
    new_data = models.JSONField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        user_str = self.user.email if self.user else "System"
        return f"{self.timestamp} - {user_str} performed {self.action}"
