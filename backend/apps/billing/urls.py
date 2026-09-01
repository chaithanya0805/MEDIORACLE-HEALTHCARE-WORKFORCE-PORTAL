from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.billing.views import InvoiceViewSet, PaymentViewSet, PaymentAdjustmentViewSet, PaymentDisputeViewSet

router = DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('payments', PaymentViewSet, basename='payment')
router.register('adjustments', PaymentAdjustmentViewSet, basename='payment-adjustment')
router.register('disputes', PaymentDisputeViewSet, basename='payment-dispute')

urlpatterns = [
    path('', include(router.urls)),
]
