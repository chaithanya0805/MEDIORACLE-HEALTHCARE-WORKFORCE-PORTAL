from django.urls import path
from apps.matching.views import ShiftMatchesView

urlpatterns = [
    path('shift/<int:shift_id>/', ShiftMatchesView.as_view(), name='shift_matches'),
    path('shift/<int:shift_id>/generate/', ShiftMatchesView.as_view(), name='shift_matches_generate'),
]
