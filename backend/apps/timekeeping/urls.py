from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.timekeeping.views import TimesheetViewSet

router = DefaultRouter()
router.register('timesheets', TimesheetViewSet, basename='timesheet')

urlpatterns = [
    path('', include(router.urls)),
]
