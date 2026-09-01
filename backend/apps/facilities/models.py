from django.db import models

class FacilityType(models.TextChoices):
    HOSPITAL = 'HOSPITAL', 'Hospital'
    CLINIC = 'CLINIC', 'Clinic'
    NURSING_HOME = 'NURSING_HOME', 'Nursing Home'
    URGENT_CARE = 'URGENT_CARE', 'Urgent Care'

class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'

class Facility(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    facility_type = models.CharField(max_length=50, choices=FacilityType.choices, default=FacilityType.HOSPITAL)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Ireland')
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    contact_person = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    operating_hours = models.CharField(max_length=100, default='24/7')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Department(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    manager = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        unique_together = ('facility', 'code')

    def __str__(self):
        return f"{self.facility.name} - {self.name}"

class Ward(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    capacity = models.IntegerField(default=20)
    required_staff = models.IntegerField(default=5)
    current_staff = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        unique_together = ('department', 'code')

    def __str__(self):
        return f"{self.department.name} - {self.name}"

class HealthcareRole(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    role = models.ForeignKey(HealthcareRole, on_delete=models.CASCADE, related_name='specialties')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('role', 'name')

    def __str__(self):
        return f"{self.role.name} - {self.name}"

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class StaffingRequirement(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    role = models.ForeignKey(HealthcareRole, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    required_workers = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default='OPEN')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Req: {self.role} at {self.ward.name} ({self.required_workers} workers)"
