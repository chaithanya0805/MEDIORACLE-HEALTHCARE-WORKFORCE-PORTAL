from rest_framework import serializers
from apps.facilities.serializers import FacilitySerializer, DepartmentSerializer, WardSerializer, HealthcareRoleSerializer, SpecialtySerializer
from apps.shifts.models import Shift, ShiftApplication, ShiftOffer, ShiftBooking
from apps.professionals.serializers import ProfessionalProfileSerializer

class ShiftSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    ward_name = serializers.CharField(source='ward.name', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    
    class Meta:
        model = Shift
        fields = [
            'id', 'facility', 'facility_name', 'department', 'department_name', 'ward', 'ward_name',
            'role', 'role_name', 'specialty', 'specialty_name', 'title', 'description', 'date',
            'start_time', 'end_time', 'location', 'required_workers', 'pay_rate', 'incentive',
            'break_duration', 'recurrence', 'status', 'notes', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_by', 'created_at', 'updated_at']

class ShiftApplicationSerializer(serializers.ModelSerializer):
    shift_details = ShiftSerializer(source='shift', read_only=True)
    professional_name = serializers.SerializerMethodField()
    professional_code = serializers.CharField(source='professional.professional_id', read_only=True)
    rating = serializers.DecimalField(source='professional.rating', max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = ShiftApplication
        fields = ['id', 'shift', 'shift_details', 'professional', 'professional_name', 'professional_code', 'rating', 'status', 'applied_at', 'decided_at', 'message']
        read_only_fields = ['id', 'applied_at', 'decided_at']

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"

class ShiftOfferSerializer(serializers.ModelSerializer):
    shift_details = ShiftSerializer(source='shift', read_only=True)
    professional_name = serializers.SerializerMethodField()

    class Meta:
        model = ShiftOffer
        fields = ['id', 'shift', 'shift_details', 'professional', 'professional_name', 'status', 'offered_at', 'expires_at']
        read_only_fields = ['id', 'offered_at']

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"

class ShiftBookingSerializer(serializers.ModelSerializer):
    shift_details = ShiftSerializer(source='shift', read_only=True)
    professional_details = ProfessionalProfileSerializer(source='professional', read_only=True)
    
    class Meta:
        model = ShiftBooking
        fields = [
            'id', 'shift', 'shift_details', 'professional', 'professional_details', 'status',
            'confirmed_at', 'confirmed_by', 'compliance_checked_at', 'compliance_override_reason', 'compliance_overridden_by'
        ]
        read_only_fields = ['id', 'confirmed_at', 'confirmed_by', 'compliance_checked_at', 'compliance_overridden_by']
