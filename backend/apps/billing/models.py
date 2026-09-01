from django.db import models
from django.conf import settings
from apps.facilities.models import Facility
from apps.shifts.models import Shift
from apps.timekeeping.models import Timesheet

class InvoiceStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    ISSUED = 'ISSUED', 'Issued'
    PENDING = 'PENDING', 'Pending'
    PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
    PAID = 'PAID', 'Paid'
    OVERDUE = 'OVERDUE', 'Overdue'
    DISPUTED = 'DISPUTED', 'Disputed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='invoices')
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    due_date = models.DateField()
    status = models.CharField(max_length=30, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} ({self.status})"

class InvoiceLineItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='line_items')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=6, decimal_places=2)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    incentive = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    overtime = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Line Item for {self.invoice.invoice_number}"

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    PAID = 'PAID', 'Paid'
    FAILED = 'FAILED', 'Failed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    DISPUTED = 'DISPUTED', 'Disputed'

class Payment(models.Model):
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='payments')
    timesheet = models.OneToOneField(Timesheet, on_delete=models.CASCADE, related_name='payment', unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='BANK_TRANSFER')
    status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    reference = models.CharField(max_length=100, unique=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.reference} (€{self.amount})"

class PaymentAdjustment(models.Model):
    professional = models.ForeignKey('professionals.ProfessionalProfile', on_delete=models.CASCADE, related_name='adjustments')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='adjustments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjustment of €{self.amount} for {self.professional}"

class DisputeStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    REVIEW = 'REVIEW', 'Review'
    EVIDENCE = 'EVIDENCE', 'Evidence'
    DECISION = 'DECISION', 'Decision'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'

class PaymentDispute(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255)
    description = models.TextField()
    evidence = models.CharField(max_length=255, null=True, blank=True, help_text="File upload or document link")
    status = models.CharField(max_length=30, choices=DisputeStatus.choices, default=DisputeStatus.OPEN)
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_disputes')
    resolution = models.TextField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dispute on {self.shift.title} - Status: {self.status}"
