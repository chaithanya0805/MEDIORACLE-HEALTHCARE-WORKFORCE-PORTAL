from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from apps.accounts.permissions import IsFacilityAdmin, IsProfessional
from apps.accounts.models import Role
from apps.shifts.models import Shift, ShiftApplication, ShiftOffer, ShiftBooking, ShiftStatus, ApplicationStatus, OfferStatus, BookingStatus
from apps.shifts.serializers import ShiftSerializer, ShiftApplicationSerializer, ShiftOfferSerializer, ShiftBookingSerializer
from apps.professionals.models import ProfessionalProfile
from apps.compliance.services import ComplianceService
from apps.scheduling.services import SchedulingConflictEngine
from apps.timekeeping.models import Timesheet, TimesheetStatus
from apps.audit.models import AuditEvent
from django.contrib.contenttypes.models import ContentType

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    filterset_fields = ['facility', 'department', 'ward', 'role', 'specialty', 'status', 'date']
    search_fields = ['title', 'location']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsFacilityAdmin])
    def publish(self, request, pk=None):
        shift = self.get_object()
        if shift.status != ShiftStatus.DRAFT:
            return Response({"success": False, "message": "Only draft shifts can be published"}, status=status.HTTP_400_BAD_REQUEST)
        shift.status = ShiftStatus.POSTED
        shift.save()
        
        AuditEvent.objects.create(
            user=request.user,
            action="SHIFT_PUBLISH",
            object_type=ContentType.objects.get_for_model(shift),
            object_id=shift.id,
            previous_data={"status": "DRAFT"},
            new_data={"status": "POSTED"},
            reason="Shift published to job board"
        )
        return Response({"success": True, "message": "Shift published successfully", "data": ShiftSerializer(shift).data})

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def apply(self, request, pk=None):
        shift = self.get_object()
        if shift.status not in [ShiftStatus.POSTED, ShiftStatus.PARTIALLY_FILLED]:
            return Response({"success": False, "message": "This shift is not accepting applications"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            professional = request.user.professional_profile
        except ProfessionalProfile.DoesNotExist:
            import random
            from apps.facilities.models import HealthcareRole
            
            # Generate unique professional ID
            prof_id = f"PRO-{random.randint(10000, 99999)}"
            while ProfessionalProfile.objects.filter(professional_id=prof_id).exists():
                prof_id = f"PRO-{random.randint(10000, 99999)}"
                
            # Default to HCA role if available
            default_role = HealthcareRole.objects.filter(name='Healthcare Assistant').first()
            
            professional = ProfessionalProfile.objects.create(
                user=request.user,
                professional_id=prof_id,
                role=default_role,
                location='Dublin',
                phone=request.user.phone or '+353870000000',
                email=request.user.email
            )
        
        if ShiftApplication.objects.filter(shift=shift, professional=professional).exists():
            return Response({"success": False, "message": "You have already applied to this shift"}, status=status.HTTP_400_BAD_REQUEST)

        app = ShiftApplication.objects.create(
            shift=shift,
            professional=professional,
            status=ApplicationStatus.APPLIED
        )

        return Response({"success": True, "message": "Application submitted successfully", "data": ShiftApplicationSerializer(app).data})

    @action(detail=True, methods=['post'], permission_classes=[IsFacilityAdmin])
    def offer(self, request, pk=None):
        shift = self.get_object()
        professional_id = request.data.get('professional_id')
        if not professional_id:
            return Response({"success": False, "message": "professional_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            professional = ProfessionalProfile.objects.get(id=professional_id)
        except ProfessionalProfile.DoesNotExist:
            return Response({"success": False, "message": "Professional not found"}, status=status.HTTP_404_NOT_FOUND)

        offer = ShiftOffer.objects.create(
            shift=shift,
            professional=professional,
            status=OfferStatus.PENDING,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        ShiftApplication.objects.filter(shift=shift, professional=professional).update(status=ApplicationStatus.OFFERED)

        return Response({"success": True, "message": "Offer sent successfully", "data": ShiftOfferSerializer(offer).data})

    @action(detail=True, methods=['post'], permission_classes=[IsFacilityAdmin])
    def confirm_booking(self, request, pk=None):
        shift = self.get_object()
        professional_id = request.data.get('professional_id')
        override_reason = request.data.get('override_reason', '')
        
        if not professional_id:
            return Response({"success": False, "message": "professional_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            professional = ProfessionalProfile.objects.get(id=professional_id)
        except ProfessionalProfile.DoesNotExist:
            return Response({"success": False, "message": "Professional not found"}, status=status.HTTP_404_NOT_FOUND)

        compliance = ComplianceService.check_professional_for_shift(professional, shift)
        if not compliance['eligible']:
            if not override_reason:
                return Response({
                    "success": False,
                    "message": "Compliance check failed. Authorized override requires a documented reason.",
                    "compliance": compliance
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                from apps.compliance.models import ComplianceAudit
                ComplianceAudit.objects.create(
                    user=request.user,
                    professional=professional,
                    shift=shift,
                    reason=override_reason
                )

        conflict_res = SchedulingConflictEngine.check_conflicts(professional, shift)
        if conflict_res['conflict']:
            return Response({
                "success": False,
                "message": f"Scheduling conflict: {conflict_res['message']}"
            }, status=status.HTTP_400_BAD_REQUEST)

        booking, created = ShiftBooking.objects.get_or_create(
            shift=shift,
            professional=professional,
            defaults={
                "status": BookingStatus.CONFIRMED,
                "confirmed_by": request.user,
                "compliance_checked_at": timezone.now(),
                "compliance_override_reason": override_reason if not compliance['eligible'] else '',
                "compliance_overridden_by": request.user if (not compliance['eligible'] and override_reason) else None
            }
        )

        if not created:
            return Response({"success": False, "message": "Booking already exists"}, status=status.HTTP_400_BAD_REQUEST)

        shift.status = ShiftStatus.FILLED
        shift.save()

        ShiftApplication.objects.filter(shift=shift, professional=professional).update(status=ApplicationStatus.ACCEPTED)

        Timesheet.objects.get_or_create(
            shift=shift,
            professional=professional,
            defaults={
                "status": TimesheetStatus.DRAFT
            }
        )

        AuditEvent.objects.create(
            user=request.user,
            action="SHIFT_BOOKING_CONFIRM",
            object_type=ContentType.objects.get_for_model(booking),
            object_id=booking.id,
            previous_data={"status": "OFFERED"},
            new_data={"status": "CONFIRMED"},
            reason=f"Booking confirmed for {professional.user.email}. Compliance check status: {'overridden' if override_reason else 'passed'}."
        )

        return Response({
            "success": True,
            "message": "Booking confirmed successfully",
            "data": ShiftBookingSerializer(booking).data
        })

class ShiftApplicationViewSet(viewsets.ModelViewSet):
    queryset = ShiftApplication.objects.all()
    serializer_class = ShiftApplicationSerializer
    filterset_fields = ['shift', 'professional', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return ShiftApplication.objects.filter(professional__user=user)
        return ShiftApplication.objects.all()

class ShiftOfferViewSet(viewsets.ModelViewSet):
    queryset = ShiftOffer.objects.all()
    serializer_class = ShiftOfferSerializer
    filterset_fields = ['shift', 'professional', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return ShiftOffer.objects.filter(professional__user=user, status=OfferStatus.PENDING)
        return ShiftOffer.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def accept(self, request, pk=None):
        offer = self.get_object()
        if offer.status != OfferStatus.PENDING:
            return Response({"success": False, "message": "Offer is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        offer.status = OfferStatus.ACCEPTED
        offer.save()

        ShiftApplication.objects.filter(shift=offer.shift, professional=offer.professional).update(status=ApplicationStatus.ACCEPTED)

        return Response({"success": True, "message": "Offer accepted. Awaiting final confirmation.", "data": ShiftOfferSerializer(offer).data})

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def reject(self, request, pk=None):
        offer = self.get_object()
        if offer.status != OfferStatus.PENDING:
            return Response({"success": False, "message": "Offer is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        
        offer.status = OfferStatus.REJECTED
        offer.save()

        ShiftApplication.objects.filter(shift=offer.shift, professional=offer.professional).update(status=ApplicationStatus.REJECTED)

        return Response({"success": True, "message": "Offer rejected successfully"})

class ShiftBookingViewSet(viewsets.ModelViewSet):
    queryset = ShiftBooking.objects.all()
    serializer_class = ShiftBookingSerializer
    filterset_fields = ['shift', 'professional', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return ShiftBooking.objects.filter(professional__user=user)
        return ShiftBooking.objects.all()
