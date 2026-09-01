from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.shifts.views import ShiftViewSet, ShiftApplicationViewSet, ShiftOfferViewSet, ShiftBookingViewSet

router = DefaultRouter()
router.register('shifts', ShiftViewSet, basename='shift')
router.register('applications', ShiftApplicationViewSet, basename='shift-application')
router.register('offers', ShiftOfferViewSet, basename='shift-offer')
router.register('bookings', ShiftBookingViewSet, basename='shift-booking')

urlpatterns = [
    path('', include(router.urls)),
]
