from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.accounts.permissions import IsFacilityAdmin
from apps.accounts.models import Role
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty, Skill, StaffingRequirement
from apps.facilities.serializers import (
    FacilitySerializer, DepartmentSerializer, WardSerializer,
    HealthcareRoleSerializer, SpecialtySerializer, SkillSerializer,
    StaffingRequirementSerializer
)

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        return Facility.objects.all()

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filterset_fields = ['facility']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filterset_fields = ['department', 'department__facility']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class HealthcareRoleViewSet(viewsets.ModelViewSet):
    queryset = HealthcareRole.objects.all()
    serializer_class = HealthcareRoleSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    filterset_fields = ['role']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

class StaffingRequirementViewSet(viewsets.ModelViewSet):
    queryset = StaffingRequirement.objects.all()
    serializer_class = StaffingRequirementSerializer
    filterset_fields = ['facility', 'department', 'ward', 'status']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsFacilityAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
