from rest_framework import serializers
from apps.facilities.serializers import HealthcareRoleSerializer, SpecialtySerializer, FacilitySerializer
from apps.professionals.models import (
    ProfessionalProfile, Qualification, WorkHistory, ProfessionalSkill,
    ProfessionalAvailability, ProfessionalPreference, ProfessionalInsurance,
    ProfessionalDocument, CredentialType, Credential
)

class CredentialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CredentialType
        fields = '__all__'

class CredentialSerializer(serializers.ModelSerializer):
    credential_type_name = serializers.CharField(source='credential_type.name', read_only=True)
    credential_type_code = serializers.CharField(source='credential_type.code', read_only=True)
    expiry_days = serializers.IntegerField(read_only=True)
    calculated_status = serializers.CharField(read_only=True)
    professional_name = serializers.SerializerMethodField()

    class Meta:
        model = Credential
        fields = [
            'id', 'professional', 'professional_name', 'credential_type', 'credential_type_name', 'credential_type_code',
            'credential_number', 'issuing_authority', 'issue_date', 'expiry_date', 'document',
            'verification_status', 'verified_by', 'verified_at', 'notes',
            'expiry_days', 'calculated_status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['verified_by', 'verified_at']

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'

class WorkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkHistory
        fields = '__all__'

class ProfessionalSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    
    class Meta:
        model = ProfessionalSkill
        fields = ['id', 'professional', 'skill', 'skill_name']

class ProfessionalAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalAvailability
        fields = '__all__'

class ProfessionalPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalPreference
        fields = '__all__'

class ProfessionalInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalInsurance
        fields = '__all__'

class ProfessionalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalDocument
        fields = '__all__'

class ProfessionalProfileSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    specialty_name = serializers.CharField(source='specialty.name', read_only=True)
    
    qualifications = QualificationSerializer(many=True, read_only=True)
    work_histories = WorkHistorySerializer(many=True, read_only=True)
    skills = ProfessionalSkillSerializer(many=True, read_only=True)
    availabilities = ProfessionalAvailabilitySerializer(many=True, read_only=True)
    preferences = ProfessionalPreferenceSerializer(read_only=True)
    credentials = CredentialSerializer(many=True, read_only=True)

    class Meta:
        model = ProfessionalProfile
        fields = [
            'id', 'user', 'user_first_name', 'user_last_name', 'user_email', 'profile_photo', 'professional_id',
            'role', 'role_name', 'specialty', 'specialty_name', 'location', 'address', 'phone', 'email',
            'years_experience', 'bio', 'languages', 'availability_status', 'preferred_rate', 'minimum_rate',
            'preferred_commute_distance', 'preferred_facilities', 'rating', 'reliability_score', 'performance_score',
            'qualifications', 'work_histories', 'skills', 'availabilities', 'preferences', 'credentials',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'professional_id', 'rating', 'reliability_score', 'performance_score', 'created_at', 'updated_at']
