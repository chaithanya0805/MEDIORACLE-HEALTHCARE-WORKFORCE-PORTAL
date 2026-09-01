from rest_framework.permissions import BasePermission
from apps.accounts.models import Role

class HasRole(BasePermission):
    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == Role.SUPER_ADMIN:
            return True
        allowed = getattr(view, 'allowed_roles', self.allowed_roles)
        if not allowed:
            return True
        return request.user.role in allowed

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.SUPER_ADMIN

class IsFacilityAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in [Role.SUPER_ADMIN, Role.FACILITY_ADMIN, Role.HR_WORKFORCE_MANAGER]

class IsProfessional(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == Role.PROFESSIONAL

class IsComplianceOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in [Role.SUPER_ADMIN, Role.COMPLIANCE_OFFICER]

class IsPayrollBilling(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in [Role.SUPER_ADMIN, Role.PAYROLL_BILLING]
