from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.compliance.views import ComplianceRuleViewSet, ComplianceCheckView

router = DefaultRouter()
router.register('rules', ComplianceRuleViewSet, basename='compliance-rule')

urlpatterns = [
    path('', include(router.urls)),
    path('check/', ComplianceCheckView.as_view(), name='compliance_check'),
]
