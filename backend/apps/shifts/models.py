from django.db import models
from django.conf import settings
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty

class ShiftStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    POSTED = 'POSTED', 'Posted'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED', 'Partially Filled'
    FILLED = 'FILLED', 'Filled'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    DISPUTED = 'DISPUTED', 'Disputed'

class RecurrenceType(models.TextChoices):
    NONE = 'NONE', 'None'
    DAILY = 'DAILY', 'Daily'
    WEEKLY = 'WEEKLY', 'Weekly'

class Shift(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='shifts')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='shifts')
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='shifts')
    role = models.ForeignKey(HealthcareRole, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, null=True, blank=True)
    required_workers = models.IntegerField(default=1)
    pay_rate = models.DecimalField(max_digits=8, decimal_places=2)
    incentive = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    break_duration = models.IntegerField(default=30, help_text="Break duration in minutes")
    recurrence = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.NONE)
    status = models.CharField(max_length=30, choices=ShiftStatus.choices, default=ShiftStatus.DRAFT)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date} ({self.status})"

class ApplicationStatus(models.TextChoices):
    APPLIED = 'APPLIED', 'Applied'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
    OFFERED = 'OFFERED', 'Offered'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    REJECTED = 'REJECTED', 'Rejected'
    WITHDRAWN = 'WITHDRAWN', 'Withdrawn'
    EXPIRED = 'EXPIRED', 'Expired'

class ShiftApplication(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='applications')
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('shift', 'professional')

    def __str__(self):
        return f"{self.professional} -> {self.shift.title} ({self.status})"

class OfferStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    REJECTED = 'REJECTED', 'Rejected'
    EXPIRED = 'EXPIRED', 'Expired'

class ShiftOffer(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='offers')
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='offers')
    status = models.CharField(max_length=30, choices=OfferStatus.choices, default=OfferStatus.PENDING)
    offered_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Offer to {self.professional} for {self.shift.title}"

class BookingStatus(models.TextChoices):
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    NO_SHOW = 'NO_SHOW', 'No Show'

class ShiftBooking(models.Model):
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='bookings')
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=30, choices=BookingStatus.choices, default=BookingStatus.CONFIRMED)
    confirmed_at = models.DateTimeField(auto_now_add=True)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    compliance_checked_at = models.DateTimeField(null=True, blank=True)
    compliance_override_reason = models.TextField(null=True, blank=True)
    compliance_overridden_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compliance_overrides')

    def __str__(self):
        return f"Booking: {self.professional} for {self.shift.title} ({self.status})"
