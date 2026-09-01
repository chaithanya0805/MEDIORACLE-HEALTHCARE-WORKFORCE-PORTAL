from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.accounts.permissions import IsComplianceOfficer
from apps.compliance.models import ComplianceRule
from apps.compliance.services import ComplianceService
from apps.professionals.models import ProfessionalProfile
from apps.shifts.models import Shift
from rest_framework import serializers

class ComplianceRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    credential_type_name = serializers.CharField(source='credential_type.name', read_only=True)

    class Meta:
        model = ComplianceRule
        fields = '__all__'

class ComplianceRuleViewSet(viewsets.ModelViewSet):
    queryset = ComplianceRule.objects.all()
    serializer_class = ComplianceRuleSerializer
    filterset_fields = ['role', 'facility']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsComplianceOfficer]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ComplianceCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        professional_id = request.data.get('professional_id')
        shift_id = request.data.get('shift_id')

        if not professional_id or not shift_id:
            return Response({"success": False, "message": "professional_id and shift_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professional = ProfessionalProfile.objects.get(id=professional_id)
            shift = Shift.objects.get(id=shift_id)
        except (ProfessionalProfile.DoesNotExist, Shift.DoesNotExist):
            return Response({"success": False, "message": "Professional or Shift not found"}, status=status.HTTP_404_NOT_FOUND)

        check_res = ComplianceService.check_professional_for_shift(professional, shift)
        return Response({
            "success": True,
            "data": check_res
        })
