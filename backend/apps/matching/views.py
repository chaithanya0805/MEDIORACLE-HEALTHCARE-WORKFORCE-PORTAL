from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.shifts.models import Shift
from apps.professionals.models import ProfessionalProfile
from apps.matching.services import MatchingService

class ShiftMatchesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, shift_id):
        try:
            shift = Shift.objects.get(id=shift_id)
        except Shift.DoesNotExist:
            return Response({"success": False, "message": "Shift not found"}, status=status.HTTP_404_NOT_FOUND)

        candidates = ProfessionalProfile.objects.filter(role=shift.role)
        matches = []
        for candidate in candidates:
            match_details = MatchingService.calculate_match(candidate, shift)
            
            matches.append({
                "professional_id": candidate.id,
                "professional_name": f"{candidate.user.first_name} {candidate.user.last_name}",
                "professional_code": candidate.professional_id,
                "specialty": candidate.specialty.name if candidate.specialty else '',
                "rating": candidate.rating,
                "reliability_score": candidate.reliability_score,
                "match_score": match_details['total_score'],
                "details": match_details
            })

        matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
        return Response({
            "success": True,
            "data": matches
        })

    def post(self, request, shift_id):
        return self.get(request, shift_id)
