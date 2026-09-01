from rest_framework import viewsets
from apps.accounts.permissions import IsSuperAdmin
from apps.audit.models import AuditEvent
from apps.audit.serializers import AuditEventSerializer

class AuditEventViewSet(viewsets.ModelViewSet):
    queryset = AuditEvent.objects.all().order_by('-timestamp')
    serializer_class = AuditEventSerializer
    permission_classes = [IsSuperAdmin]
    filterset_fields = ['action', 'user']
