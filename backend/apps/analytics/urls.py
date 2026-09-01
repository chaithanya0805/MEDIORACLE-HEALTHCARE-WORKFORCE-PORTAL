from django.urls import path
from apps.analytics.views import FacilityAnalyticsView, AgencyAnalyticsView, WhatIfScenarioView

urlpatterns = [
    path('facility/', FacilityAnalyticsView.as_view(), name='analytics_facility'),
    path('agency/', AgencyAnalyticsView.as_view(), name='analytics_agency'),
    path('what-if/', WhatIfScenarioView.as_view(), name='analytics_what_if'),
]
