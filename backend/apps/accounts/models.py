from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Role(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    FACILITY_ADMIN = 'FACILITY_ADMIN', 'Facility Admin'
    HR_WORKFORCE_MANAGER = 'HR_WORKFORCE_MANAGER', 'HR & Workforce Manager'
    WARD_LEADER = 'WARD_LEADER', 'Ward Leader'
    PROFESSIONAL = 'PROFESSIONAL', 'Healthcare Professional'
    RECRUITER = 'RECRUITER', 'Recruiter'
    COMPLIANCE_OFFICER = 'COMPLIANCE_OFFICER', 'Compliance Officer'
    PAYROLL_BILLING = 'PAYROLL_BILLING', 'Payroll & Billing'
    SUPPORT_AGENT = 'SUPPORT_AGENT', 'Support Agent'
    REGIONAL_COORDINATOR = 'REGIONAL_COORDINATOR', 'Regional Coordinator'
    BUSINESS_LEADER = 'BUSINESS_LEADER', 'Business Leader'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.SUPER_ADMIN)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.PROFESSIONAL)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
