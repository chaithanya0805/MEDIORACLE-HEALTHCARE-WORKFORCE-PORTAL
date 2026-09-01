import uuid
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsComplianceOfficer
from apps.accounts.models import Role
from apps.professionals.models import (
    ProfessionalProfile, Qualification, WorkHistory, ProfessionalSkill,
    ProfessionalAvailability, ProfessionalPreference, ProfessionalInsurance,
    ProfessionalDocument, CredentialType, Credential, CredentialStatus
)
from apps.professionals.serializers import (
    ProfessionalProfileSerializer, QualificationSerializer, WorkHistorySerializer,
    ProfessionalSkillSerializer, ProfessionalAvailabilitySerializer, ProfessionalPreferenceSerializer,
    ProfessionalInsuranceSerializer, ProfessionalDocumentSerializer, CredentialTypeSerializer,
    CredentialSerializer
)

class ProfessionalProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalProfile.objects.all()
    serializer_class = ProfessionalProfileSerializer
    filterset_fields = ['role', 'specialty', 'availability_status']
    search_fields = ['user__first_name', 'user__last_name', 'location', 'professional_id']

    def perform_create(self, serializer):
        prof_id = f"PRO-{uuid.uuid4().hex[:8].upper()}"
        serializer.save(user=self.request.user, professional_id=prof_id, email=self.request.user.email)

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return ProfessionalProfile.objects.filter(user=user)
        return ProfessionalProfile.objects.all()

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return Qualification.objects.filter(professional__user=user)
        return Qualification.objects.all()

class WorkHistoryViewSet(viewsets.ModelViewSet):
    queryset = WorkHistory.objects.all()
    serializer_class = WorkHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return WorkHistory.objects.filter(professional__user=user)
        return WorkHistory.objects.all()

class ProfessionalSkillViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalSkill.objects.all()
    serializer_class = ProfessionalSkillSerializer
    permission_classes = [IsAuthenticated]

class ProfessionalAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalAvailability.objects.all()
    serializer_class = ProfessionalAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return ProfessionalAvailability.objects.filter(professional__user=user)
        return ProfessionalAvailability.objects.all()

class ProfessionalPreferenceViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalPreference.objects.all()
    serializer_class = ProfessionalPreferenceSerializer
    permission_classes = [IsAuthenticated]

class ProfessionalInsuranceViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalInsurance.objects.all()
    serializer_class = ProfessionalInsuranceSerializer
    permission_classes = [IsAuthenticated]

class ProfessionalDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalDocument.objects.all()
    serializer_class = ProfessionalDocumentSerializer
    permission_classes = [IsAuthenticated]

class CredentialTypeViewSet(viewsets.ModelViewSet):
    queryset = CredentialType.objects.all()
    serializer_class = CredentialTypeSerializer
    permission_classes = [IsAuthenticated]

class CredentialViewSet(viewsets.ModelViewSet):
    queryset = Credential.objects.all()
    serializer_class = CredentialSerializer
    filterset_fields = ['verification_status', 'credential_type__code', 'professional']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return Credential.objects.filter(professional__user=user)
        return Credential.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[IsComplianceOfficer])
    def verify(self, request, pk=None):
        credential = self.get_object()
        status_val = request.data.get('status')
        notes = request.data.get('notes', '')
        
        if status_val not in [CredentialStatus.VERIFIED, CredentialStatus.REJECTED]:
            return Response({"success": False, "message": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
        
        credential.verification_status = status_val
        credential.verified_by = request.user
        credential.verified_at = timezone.now()
        credential.notes = notes
        credential.save()

        from apps.audit.models import AuditEvent
        from django.contrib.contenttypes.models import ContentType
        AuditEvent.objects.create(
            user=request.user,
            action=f"CREDENTIAL_VERIFICATION_{status_val}",
            object_type=ContentType.objects.get_for_model(credential),
            object_id=credential.id,
            previous_data={"status": "SUBMITTED"},
            new_data={"status": status_val, "notes": notes},
            reason=f"Credential reviewed and marked as {status_val}"
        )

        return Response({
            "success": True,
            "message": f"Credential has been marked as {status_val}",
            "data": CredentialSerializer(credential).data
        })

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        qs = self.get_queryset()
        pending = qs.filter(verification_status=CredentialStatus.PENDING).count()
        submitted = qs.filter(verification_status=CredentialStatus.SUBMITTED).count()
        
        verified = qs.filter(verification_status=CredentialStatus.VERIFIED)
        expired_count = 0
        expiring_30 = 0
        expiring_60 = 0
        expiring_90 = 0
        valid_count = 0

        for cred in verified:
            days = cred.expiry_days
            if days <= 0:
                expired_count += 1
            elif days <= 30:
                expiring_30 += 1
            elif days <= 60:
                expiring_60 += 1
            elif days <= 90:
                expiring_90 += 1
            else:
                valid_count += 1
        
        rejected = qs.filter(verification_status=CredentialStatus.REJECTED).count()

        return Response({
            "success": True,
            "data": {
                "valid": valid_count,
                "expiring_soon": expiring_30 + expiring_60 + expiring_90,
                "expiring_30": expiring_30,
                "expiring_60": expiring_60,
                "expiring_90": expiring_90,
                "expired": expired_count,
                "pending": pending + submitted,
                "rejected": rejected
            }
        })
