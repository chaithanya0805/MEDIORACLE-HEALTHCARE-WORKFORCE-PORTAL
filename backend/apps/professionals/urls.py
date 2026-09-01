from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.professionals.views import (
    ProfessionalProfileViewSet, QualificationViewSet, WorkHistoryViewSet,
    ProfessionalSkillViewSet, ProfessionalAvailabilityViewSet, ProfessionalPreferenceViewSet,
    ProfessionalInsuranceViewSet, ProfessionalDocumentViewSet, CredentialTypeViewSet,
    CredentialViewSet
)

router = DefaultRouter()
router.register('profiles', ProfessionalProfileViewSet, basename='professional-profile')
router.register('qualifications', QualificationViewSet, basename='qualification')
router.register('work-histories', WorkHistoryViewSet, basename='work-history')
router.register('skills', ProfessionalSkillViewSet, basename='professional-skill')
router.register('availabilities', ProfessionalAvailabilityViewSet, basename='professional-availability')
router.register('preferences', ProfessionalPreferenceViewSet, basename='professional-preference')
router.register('insurances', ProfessionalInsuranceViewSet, basename='professional-insurance')
router.register('documents', ProfessionalDocumentViewSet, basename='professional-document')
router.register('credential-types', CredentialTypeViewSet, basename='credential-type')
router.register('credentials', CredentialViewSet, basename='credential')

urlpatterns = [
    path('', include(router.urls)),
]
