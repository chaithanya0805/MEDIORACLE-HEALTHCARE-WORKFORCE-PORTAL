import datetime
from django.db import models
from django.conf import settings
from apps.facilities.models import HealthcareRole, Specialty, Skill, Facility

class AvailabilityStatus(models.TextChoices):
    AVAILABLE = 'AVAILABLE', 'Available'
    BUSY = 'BUSY', 'Busy'
    ON_LEAVE = 'ON_LEAVE', 'On Leave'
    UNAVAILABLE = 'UNAVAILABLE', 'Unavailable'

class ProfessionalProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='professional_profile')
    profile_photo = models.ImageField(upload_to='professionals/', null=True, blank=True)
    professional_id = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(HealthcareRole, on_delete=models.SET_NULL, null=True, blank=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    years_experience = models.IntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    languages = models.CharField(max_length=200, default='English')
    availability_status = models.CharField(max_length=30, choices=AvailabilityStatus.choices, default=AvailabilityStatus.AVAILABLE)
    preferred_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    minimum_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    preferred_commute_distance = models.IntegerField(default=50, help_text="in km")
    preferred_facilities = models.ManyToManyField(Facility, blank=True, related_name='preferred_by_professionals')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    reliability_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    performance_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.professional_id})"

class Qualification(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='qualifications')
    name = models.CharField(max_length=200)
    issuing_body = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default='ACTIVE')
    document = models.FileField(upload_to='qualifications/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.professional}"

class WorkHistory(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='work_histories')
    facility_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.role} at {self.facility_name}"

class ProfessionalSkill(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('professional', 'skill')

class ProfessionalAvailability(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    SHIFT_TYPES = (
        ('DAY', 'Day'),
        ('NIGHT', 'Night'),
        ('EVENING', 'Evening'),
    )
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    shift_type = models.CharField(max_length=20, choices=SHIFT_TYPES)

    class Meta:
        unique_together = ('professional', 'day_of_week', 'shift_type')

class ProfessionalPreference(models.Model):
    professional = models.OneToOneField(ProfessionalProfile, on_delete=models.CASCADE, related_name='preferences')
    preferred_shift_types = models.CharField(max_length=200, default='DAY,NIGHT,EVENING')
    preferred_days = models.CharField(max_length=200, default='0,1,2,3,4,5,6')

class ProfessionalInsurance(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='insurances')
    provider = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    document = models.FileField(upload_to='insurance/', null=True, blank=True)

class ProfessionalDocument(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CredentialType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True) # NMBI, BLS, ACLS, PALS, GARDA, IMMUNIZATION, TRAINING, INSURANCE, LANGUAGE, OTHER
    description = models.TextField(null=True, blank=True)
    required_by_default = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CredentialStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    VERIFIED = 'VERIFIED', 'Verified'
    REJECTED = 'REJECTED', 'Rejected'
    EXPIRED = 'EXPIRED', 'Expired'
    RESTRICTED = 'RESTRICTED', 'Restricted'

class Credential(models.Model):
    professional = models.ForeignKey(ProfessionalProfile, on_delete=models.CASCADE, related_name='credentials')
    credential_type = models.ForeignKey(CredentialType, on_delete=models.CASCADE)
    credential_number = models.CharField(max_length=100)
    issuing_authority = models.CharField(max_length=200)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    document = models.FileField(upload_to='credentials/')
    verification_status = models.CharField(max_length=30, choices=CredentialStatus.choices, default=CredentialStatus.PENDING)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_credentials')
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.credential_type.name} - {self.professional}"

    @property
    def expiry_days(self):
        if not self.expiry_date:
            return 999
        delta = self.expiry_date - datetime.date.today()
        return delta.days

    @property
    def calculated_status(self):
        if self.verification_status == CredentialStatus.VERIFIED:
            if self.expiry_days <= 0:
                return CredentialStatus.EXPIRED
        return self.verification_status
