from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.facilities.views import (
    FacilityViewSet, DepartmentViewSet, WardViewSet,
    HealthcareRoleViewSet, SpecialtyViewSet, SkillViewSet,
    StaffingRequirementViewSet
)

router = DefaultRouter()
router.register('facilities', FacilityViewSet, basename='facility')
router.register('departments', DepartmentViewSet, basename='department')
router.register('wards', WardViewSet, basename='ward')
router.register('roles', HealthcareRoleViewSet, basename='role')
router.register('specialties', SpecialtyViewSet, basename='specialty')
router.register('skills', SkillViewSet, basename='skill')
router.register('staffing-requirements', StaffingRequirementViewSet, basename='staffing-requirement')

urlpatterns = [
    path('', include(router.urls)),
]
