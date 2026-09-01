from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from apps.accounts.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['success'] = True
        data['message'] = "Login successful"
        data['user'] = {
            'id': self.user.id,
            'name': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.email,
            'email': self.user.email,
            'role': self.user.role
        }
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "success": True,
                "message": "User registered successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "name": f"{user.first_name} {user.last_name}".strip() or user.email,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Registration failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "success": True,
            "data": serializer.data
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                "success": True,
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
        except TokenError:
            # Refresh token is already invalid/expired/blacklisted, treat as successful logout
            return Response({
                "success": True,
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Logout failed",
                "errors": {"detail": str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    "success": False,
                    "message": "Invalid old password"
                }, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                "success": True,
                "message": "Password changed successfully"
            })
        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.core.mail import send_mail
        from django.conf import settings

        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:4200')
                reset_link = f"{frontend_url}/reset-password?email={user.email}&token={token}"
                
                subject = "Nexgile MediOracle - Password Reset Request"
                message = f"Hello,\n\nYou are receiving this email because a password reset request was made for your Nexgile account.\n\nPlease click the link below to reset your password:\n{reset_link}\n\nIf you did not request a password reset, please ignore this email.\n\nRegards,\nNexgile Team"
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                # Generic response to prevent user enumeration
                pass
            except Exception as e:
                # Log but proceed with generic response
                print("Failed to send password reset email:", e)

            return Response({
                "success": True,
                "message": "If this email is registered, a password reset link has been sent."
            })
        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                if not default_token_generator.check_token(user, token):
                    return Response({
                        "success": False,
                        "message": "The reset link is invalid or has expired."
                    }, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(new_password)
                user.save()
                return Response({
                    "success": True,
                    "message": "Password has been reset successfully"
                })
            except User.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User not found"
                }, status=status.HTTP_440_NOT_FOUND if hasattr(status, 'HTTP_440_NOT_FOUND') else status.HTTP_404_NOT_FOUND)
        return Response({
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
