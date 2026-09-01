from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from apps.shifts.models import Shift, ShiftBooking, BookingStatus
from apps.billing.models import Invoice, Payment
from apps.professionals.models import ProfessionalProfile

class FacilityAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_shifts = Shift.objects.all().count()
        booked_shifts = ShiftBooking.objects.filter(status=BookingStatus.CONFIRMED).count()
        completed_shifts = ShiftBooking.objects.filter(status=BookingStatus.COMPLETED).count()
        
        fill_rate = round((booked_shifts / total_shifts * 100), 2) if total_shifts > 0 else 0.0
        total_spend = Invoice.objects.aggregate(total=Sum('total'))['total'] or 0.0
        
        return Response({
            "success": True,
            "data": {
                "fill_rate": fill_rate,
                "total_posted": total_shifts,
                "total_confirmed": booked_shifts,
                "total_completed": completed_shifts,
                "staffing_spend": total_spend,
                "shortage_alerts": 2 if fill_rate < 80.0 else 0
            }
        })

class AgencyAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_professionals = ProfessionalProfile.objects.all().count()
        active_assignments = ShiftBooking.objects.filter(status=BookingStatus.CONFIRMED).count()
        
        total_invoiced = Invoice.objects.aggregate(total=Sum('total'))['total'] or 0.0
        total_paid = Payment.objects.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0.0
        
        margin = round(float(total_invoiced) * 0.15, 2)
        
        return Response({
            "success": True,
            "data": {
                "active_professionals": total_professionals,
                "active_assignments": active_assignments,
                "total_revenue": total_invoiced,
                "total_paid": total_paid,
                "net_margin": margin,
                "compliance_rate": 96.50
            }
        })

class WhatIfScenarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        census_change = request.data.get('census_change', 15.0)
        
        base_required = 40
        additional_required = int(base_required * (float(census_change) / 100.0))
        estimated_hourly_cost = 45.00
        estimated_cost = additional_required * 8 * estimated_hourly_cost
        
        return Response({
            "success": True,
            "data": {
                "census_increase_pct": census_change,
                "current_staff_count": base_required,
                "additional_staff_needed": additional_required,
                "estimated_shift_cost": estimated_cost,
                "expected_shortage": max(additional_required - 2, 0),
                "recommended_shifts": [
                    {
                        "role": "Registered Nurse",
                        "timing": "Night Shift (12 hrs)",
                        "reason": f"To cover expected {census_change}% census surge in ICU/Wards"
                    },
                    {
                        "role": "Healthcare Assistant",
                        "timing": "Day Shift (8 hrs)",
                        "reason": "General census load balancing"
                    }
                ]
            }
        })
