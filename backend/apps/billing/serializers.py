from rest_framework import serializers
from apps.billing.models import Invoice, InvoiceLineItem, Payment, PaymentAdjustment, PaymentDispute
from apps.facilities.serializers import FacilitySerializer
from apps.shifts.serializers import ShiftSerializer

class InvoiceLineItemSerializer(serializers.ModelSerializer):
    professional_name = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceLineItem
        fields = '__all__'

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"

class InvoiceSerializer(serializers.ModelSerializer):
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    line_items = InvoiceLineItemSerializer(many=True, read_only=True)
    shift_title = serializers.CharField(source='shift.title', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'facility', 'facility_name', 'shift', 'shift_title',
            'subtotal', 'tax', 'adjustment', 'total', 'due_date', 'status',
            'line_items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'invoice_number', 'subtotal', 'tax', 'total', 'created_at', 'updated_at']

class PaymentAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAdjustment
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    professional_name = serializers.SerializerMethodField()
    timesheet_hours = serializers.DecimalField(source='timesheet.total_hours', max_digits=5, decimal_places=2, read_only=True)
    adjustments = PaymentAdjustmentSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'professional', 'professional_name', 'timesheet', 'timesheet_hours',
            'amount', 'payment_method', 'status', 'reference', 'paid_at',
            'adjustments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reference', 'created_at', 'updated_at']

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"

class PaymentDisputeSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    shift_title = serializers.CharField(source='shift.title', read_only=True)
    assigned_agent_name = serializers.SerializerMethodField()

    class Meta:
        model = PaymentDispute
        fields = '__all__'
        read_only_fields = ['id', 'assigned_agent', 'resolution', 'resolved_at', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_assigned_agent_name(self, obj):
        if obj.assigned_agent:
            return f"{obj.assigned_agent.first_name} {obj.assigned_agent.last_name}"
        return None
