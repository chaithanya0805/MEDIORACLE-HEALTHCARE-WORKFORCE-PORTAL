from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from apps.accounts.permissions import IsPayrollBilling
from apps.accounts.models import Role
from apps.billing.models import Invoice, InvoiceLineItem, Payment, PaymentAdjustment, PaymentDispute, PaymentStatus, InvoiceStatus, DisputeStatus
from apps.billing.serializers import InvoiceSerializer, PaymentSerializer, PaymentAdjustmentSerializer, PaymentDisputeSerializer
from apps.audit.models import AuditEvent
from django.contrib.contenttypes.models import ContentType

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filterset_fields = ['facility', 'status']

    def get_queryset(self):
        return Invoice.objects.all()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ['professional', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return Payment.objects.filter(professional__user=user)
        return Payment.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[IsPayrollBilling])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.status == PaymentStatus.PAID:
            return Response({"success": False, "message": "Payment has already been processed and paid"}, status=status.HTTP_400_BAD_REQUEST)
        
        import uuid
        payment.status = PaymentStatus.PAID
        payment.reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        payment.paid_at = timezone.now()
        payment.save()

        AuditEvent.objects.create(
            user=request.user,
            action="PAYMENT_PROCESS",
            object_type=ContentType.objects.get_for_model(payment),
            object_id=payment.id,
            previous_data={"status": "PENDING"},
            new_data={"status": "PAID", "reference": payment.reference},
            reason="Payment released by payroll billing officer"
        )

        return Response({
            "success": True,
            "message": "Payment processed successfully",
            "data": PaymentSerializer(payment).data
        })

class PaymentAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = PaymentAdjustment.objects.all()
    serializer_class = PaymentAdjustmentSerializer
    permission_classes = [IsPayrollBilling]

class PaymentDisputeViewSet(viewsets.ModelViewSet):
    queryset = PaymentDispute.objects.all()
    serializer_class = PaymentDisputeSerializer
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        if user.role == Role.PROFESSIONAL:
            return PaymentDispute.objects.filter(user=user)
        return PaymentDispute.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        dispute = self.get_object()
        resolution = request.data.get('resolution')
        if not resolution:
            return Response({"success": False, "message": "resolution is required"}, status=status.HTTP_400_BAD_REQUEST)

        dispute.status = DisputeStatus.RESOLVED
        dispute.resolution = resolution
        dispute.resolved_at = timezone.now()
        dispute.assigned_agent = request.user
        dispute.save()

        AuditEvent.objects.create(
            user=request.user,
            action="DISPUTE_RESOLVE",
            object_type=ContentType.objects.get_for_model(dispute),
            object_id=dispute.id,
            previous_data={"status": "OPEN"},
            new_data={"status": "RESOLVED", "resolution": resolution},
            reason="Dispute resolved by agent"
        )

        return Response({
            "success": True,
            "message": "Dispute resolved successfully",
            "data": PaymentDisputeSerializer(dispute).data
        })
