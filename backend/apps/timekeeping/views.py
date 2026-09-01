from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from apps.accounts.permissions import IsProfessional, IsFacilityAdmin
from apps.accounts.models import Role
from apps.timekeeping.models import Timesheet, ClockEvent, TimesheetCorrection, TimesheetStatus, EventType, ValidationStatus
from apps.timekeeping.serializers import TimesheetSerializer
from apps.audit.models import AuditEvent
from django.contrib.contenttypes.models import ContentType

class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    filterset_fields = ['shift', 'professional', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return Timesheet.objects.filter(professional__user=user)
        return Timesheet.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def clock_in(self, request, pk=None):
        timesheet = self.get_object()
        if timesheet.status != TimesheetStatus.DRAFT:
            return Response({"success": False, "message": "Clock-in is only allowed for draft timesheets"}, status=status.HTTP_400_BAD_REQUEST)
        if timesheet.clock_in:
            return Response({"success": False, "message": "Already clocked in"}, status=status.HTTP_400_BAD_REQUEST)

        lat = request.data.get('latitude')
        lng = request.data.get('longitude')
        timestamp = timezone.now()

        timesheet.clock_in = timestamp
        timesheet.save()

        ClockEvent.objects.create(
            timesheet=timesheet,
            event_type=EventType.CLOCK_IN,
            timestamp=timestamp,
            latitude=lat,
            longitude=lng,
            validation_status=ValidationStatus.VALID
        )

        return Response({
            "success": True,
            "message": "Clocked in successfully",
            "data": TimesheetSerializer(timesheet).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def break_start(self, request, pk=None):
        timesheet = self.get_object()
        if not timesheet.clock_in or timesheet.clock_out:
            return Response({"success": False, "message": "Break not allowed at this stage"}, status=status.HTTP_400_BAD_REQUEST)

        timestamp = timezone.now()
        ClockEvent.objects.create(
            timesheet=timesheet,
            event_type=EventType.BREAK_START,
            timestamp=timestamp,
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude')
        )
        return Response({"success": True, "message": "Break started successfully"})

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def break_end(self, request, pk=None):
        timesheet = self.get_object()
        if not timesheet.clock_in or timesheet.clock_out:
            return Response({"success": False, "message": "Break end not allowed at this stage"}, status=status.HTTP_400_BAD_REQUEST)

        last_start = ClockEvent.objects.filter(timesheet=timesheet, event_type=EventType.BREAK_START).last()
        timestamp = timezone.now()
        
        break_duration = 30
        if last_start:
            delta = timestamp - last_start.timestamp
            break_duration = max(int(delta.total_seconds() / 60), 0)

        timesheet.break_minutes += break_duration
        timesheet.save()

        ClockEvent.objects.create(
            timesheet=timesheet,
            event_type=EventType.BREAK_END,
            timestamp=timestamp,
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude')
        )
        return Response({"success": True, "message": f"Break ended successfully. Break duration: {break_duration} mins."})

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def clock_out(self, request, pk=None):
        timesheet = self.get_object()
        if not timesheet.clock_in:
            return Response({"success": False, "message": "Cannot clock out without clocking in first"}, status=status.HTTP_400_BAD_REQUEST)
        if timesheet.clock_out:
            return Response({"success": False, "message": "Already clocked out"}, status=status.HTTP_400_BAD_REQUEST)

        timestamp = timezone.now()
        timesheet.clock_out = timestamp
        
        delta = timestamp - timesheet.clock_in
        total_worked_minutes = max(int(delta.total_seconds() / 60) - timesheet.break_minutes, 0)
        hours = round(total_worked_minutes / 60.0, 2)
        
        timesheet.total_hours = hours
        if hours > 8.0:
            timesheet.overtime_hours = round(hours - 8.0, 2)
        else:
            timesheet.overtime_hours = 0.00
            
        timesheet.save()

        ClockEvent.objects.create(
            timesheet=timesheet,
            event_type=EventType.CLOCK_OUT,
            timestamp=timestamp,
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude')
        )

        return Response({
            "success": True,
            "message": "Clocked out successfully",
            "data": TimesheetSerializer(timesheet).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsProfessional])
    def submit(self, request, pk=None):
        timesheet = self.get_object()
        signature = request.data.get('signature')
        
        if not timesheet.clock_out:
            return Response({"success": False, "message": "Timesheet must be clocked out before submission"}, status=status.HTTP_400_BAD_REQUEST)
        
        timesheet.professional_signature = signature
        timesheet.status = TimesheetStatus.SUBMITTED
        timesheet.submitted_at = timezone.now()
        timesheet.save()

        return Response({
            "success": True,
            "message": "Timesheet submitted for manager approval",
            "data": TimesheetSerializer(timesheet).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsFacilityAdmin])
    def approve(self, request, pk=None):
        timesheet = self.get_object()
        if timesheet.status in [TimesheetStatus.APPROVED, TimesheetStatus.LOCKED]:
            return Response({"success": False, "message": "Timesheet is already approved or locked"}, status=status.HTTP_400_BAD_REQUEST)

        timesheet.status = TimesheetStatus.LOCKED
        timesheet.manager_approval = request.user
        timesheet.approved_at = timezone.now()
        timesheet.locked_at = timezone.now()
        timesheet.save()

        from apps.billing.models import Invoice, InvoiceLineItem, InvoiceStatus
        from decimal import Decimal
        
        pay_rate = timesheet.shift.pay_rate
        incentive = timesheet.shift.incentive
        overtime_rate = pay_rate * Decimal('1.5')
        
        regular_hours = Decimal(str(timesheet.total_hours - timesheet.overtime_hours))
        overtime_hours = Decimal(str(timesheet.overtime_hours))
        
        amount = (regular_hours * pay_rate) + (overtime_hours * overtime_rate) + incentive
        tax = amount * Decimal('0.20')
        total = amount + tax

        import uuid
        invoice = Invoice.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            facility=timesheet.shift.facility,
            shift=timesheet.shift,
            subtotal=amount,
            tax=tax,
            total=total,
            due_date=timezone.now().date() + timedelta(days=30),
            status=InvoiceStatus.ISSUED
        )

        InvoiceLineItem.objects.create(
            invoice=invoice,
            shift=timesheet.shift,
            professional=timesheet.professional,
            hours=timesheet.total_hours,
            rate=pay_rate,
            incentive=incentive,
            overtime=timesheet.overtime_hours,
            amount=amount
        )

        AuditEvent.objects.create(
            user=request.user,
            action="TIMESHEET_APPROVE",
            object_type=ContentType.objects.get_for_model(timesheet),
            object_id=timesheet.id,
            previous_data={"status": "SUBMITTED"},
            new_data={"status": "LOCKED"},
            reason="Timesheet approved and invoice generated"
        )

        return Response({
            "success": True,
            "message": "Timesheet approved and locked. Billing invoice created.",
            "data": TimesheetSerializer(timesheet).data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsFacilityAdmin])
    def correct(self, request, pk=None):
        timesheet = self.get_object()
        corrected_hours = request.data.get('total_hours')
        reason = request.data.get('reason')

        if not corrected_hours or not reason:
            return Response({"success": False, "message": "total_hours and reason are required"}, status=status.HTTP_400_BAD_REQUEST)

        original_val = f"Total Hours: {timesheet.total_hours}, Status: {timesheet.status}"
        
        timesheet.total_hours = corrected_hours
        timesheet.status = TimesheetStatus.CORRECTED
        timesheet.save()

        TimesheetCorrection.objects.create(
            timesheet=timesheet,
            original_value=original_val,
            corrected_value=f"Total Hours: {corrected_hours}, Status: CORRECTED",
            reason=reason,
            corrected_by=request.user
        )

        AuditEvent.objects.create(
            user=request.user,
            action="TIMESHEET_CORRECTION",
            object_type=ContentType.objects.get_for_model(timesheet),
            object_id=timesheet.id,
            previous_data={"total_hours": str(timesheet.total_hours)},
            new_data={"total_hours": str(corrected_hours), "status": "CORRECTED"},
            reason=reason
        )

        return Response({
            "success": True,
            "message": "Timesheet corrected successfully",
            "data": TimesheetSerializer(timesheet).data
        })
