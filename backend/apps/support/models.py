from django.db import models
from django.conf import settings
from apps.facilities.models import Facility

class CaseStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    ASSIGNED = 'ASSIGNED', 'Assigned'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    WAITING = 'WAITING', 'Waiting'
    RESOLVED = 'RESOLVED', 'Resolved'
    CLOSED = 'CLOSED', 'Closed'

class CasePriority(models.TextChoices):
    LOW = 'LOW', 'Low'
    MEDIUM = 'MEDIUM', 'Medium'
    HIGH = 'HIGH', 'High'
    URGENT = 'URGENT', 'Urgent'

class SupportCase(models.Model):
    case_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_cases')
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=100, default='General Inquiry')
    priority = models.CharField(max_length=20, choices=CasePriority.choices, default=CasePriority.MEDIUM)
    description = models.TextField()
    attachment = models.FileField(upload_to='support_attachments/', null=True, blank=True)
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    status = models.CharField(max_length=30, choices=CaseStatus.choices, default=CaseStatus.OPEN)
    resolution = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case {self.case_id} - Priority: {self.priority} - Status: {self.status}"

class SupportMessage(models.Model):
    support_case = models.ForeignKey(SupportCase, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg on Case {self.support_case.case_id} from {self.sender.email}"

class KnowledgeBaseArticle(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
