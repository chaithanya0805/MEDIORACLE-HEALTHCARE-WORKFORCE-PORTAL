from rest_framework import serializers
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty, Skill, StaffingRequirement

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class SpecialtySerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = Specialty
        fields = ['id', 'role', 'role_name', 'name', 'description']

class HealthcareRoleSerializer(serializers.ModelSerializer):
    specialties = SpecialtySerializer(many=True, read_only=True)
    
    class Meta:
        model = HealthcareRole
        fields = ['id', 'name', 'description', 'specialties']

class WardSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    facility_name = serializers.CharField(source='department.facility.name', read_only=True)
    
    class Meta:
        model = Ward
        fields = ['id', 'department', 'department_name', 'facility_name', 'name', 'code', 'capacity', 'required_staff', 'current_staff', 'status']

class DepartmentSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    wards = WardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'facility', 'facility_name', 'name', 'code', 'manager', 'status', 'wards']

class FacilitySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Facility
        fields = ['id', 'name', 'code', 'facility_type', 'address', 'city', 'state', 'country', 'postal_code', 'phone', 'email', 'contact_person', 'status', 'budget', 'operating_hours', 'departments', 'created_at', 'updated_at']

class StaffingRequirementSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)

    class Meta:
        model = StaffingRequirement
        fields = ['id', 'facility', 'facility_name', 'department', 'department_name', 'ward', 'ward_name', 'role', 'role_name', 'specialty', 'specialty_name', 'required_workers', 'status', 'start_date', 'end_date', 'created_at', 'updated_at']
