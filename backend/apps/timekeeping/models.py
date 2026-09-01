from django.db import models
from django.conf import settings
from apps.shifts.models import Shift

class TimesheetStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    CORRECTED = 'CORRECTED', 'Corrected'
    LOCKED = 'LOCKED', 'Locked'

class Timesheet(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='timesheets')
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='timesheets')
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    break_minutes = models.IntegerField(default=0)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    professional_signature = models.TextField(null=True, blank=True, help_text="Base64 or digital signature text")
    manager_approval = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_timesheets')
    status = models.CharField(max_length=30, choices=TimesheetStatus.choices, default=TimesheetStatus.DRAFT)
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shift', 'professional')

    def __str__(self):
        return f"Timesheet: {self.professional} for {self.shift.title} ({self.status})"

class EventType(models.TextChoices):
    CLOCK_IN = 'CLOCK_IN', 'Clock In'
    CLOCK_OUT = 'CLOCK_OUT', 'Clock Out'
    BREAK_START = 'BREAK_START', 'Break Start'
    BREAK_END = 'BREAK_END', 'Break End'

class ValidationStatus(models.TextChoices):
    VALID = 'VALID', 'Valid'
    FAILED_GEOFENCE = 'FAILED_GEOFENCE', 'Failed Geofence'

class ClockEvent(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='clock_events')
    event_type = models.CharField(max_length=30, choices=EventType.choices)
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    validation_status = models.CharField(max_length=30, choices=ValidationStatus.choices, default=ValidationStatus.VALID)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.event_type} - {self.timestamp} for {self.timesheet}"

class TimesheetCorrection(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='corrections')
    original_value = models.TextField()
    corrected_value = models.TextField()
    reason = models.TextField()
    corrected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    corrected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correction on {self.timesheet} by {self.corrected_by}"
