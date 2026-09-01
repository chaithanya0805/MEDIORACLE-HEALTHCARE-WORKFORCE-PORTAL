from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import Role

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'role', 'profile_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', Role.PROFESSIONAL)
        )
        
        if user.role == Role.PROFESSIONAL:
            from apps.professionals.models import ProfessionalProfile
            from apps.facilities.models import HealthcareRole
            import random
            
            # Generate unique professional ID
            prof_id = f"PRO-{random.randint(10000, 99999)}"
            while ProfessionalProfile.objects.filter(professional_id=prof_id).exists():
                prof_id = f"PRO-{random.randint(10000, 99999)}"
                
            # Default to HCA role if available
            default_role = HealthcareRole.objects.filter(name='Healthcare Assistant').first()
            
            ProfessionalProfile.objects.create(
                user=user,
                professional_id=prof_id,
                role=default_role,
                location='Dublin',
                phone=user.phone or '+353870000000',
                email=user.email
            )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
