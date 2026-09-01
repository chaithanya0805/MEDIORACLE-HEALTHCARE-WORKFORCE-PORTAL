from rest_framework import serializers
from apps.timekeeping.models import Timesheet, ClockEvent, TimesheetCorrection
from apps.shifts.serializers import ShiftSerializer

class ClockEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockEvent
        fields = '__all__'

class TimesheetCorrectionSerializer(serializers.ModelSerializer):
    corrected_by_name = serializers.SerializerMethodField()

    class Meta:
        model = TimesheetCorrection
        fields = '__all__'

    def get_corrected_by_name(self, obj):
        return f"{obj.corrected_by.first_name} {obj.corrected_by.last_name}"

class TimesheetSerializer(serializers.ModelSerializer):
    shift_details = ShiftSerializer(source='shift', read_only=True)
    professional_name = serializers.SerializerMethodField()
    clock_events = ClockEventSerializer(many=True, read_only=True)
    corrections = TimesheetCorrectionSerializer(many=True, read_only=True)

    class Meta:
        model = Timesheet
        fields = [
            'id', 'shift', 'shift_details', 'professional', 'professional_name',
            'clock_in', 'clock_out', 'break_minutes', 'total_hours', 'overtime_hours',
            'professional_signature', 'manager_approval', 'status', 'submitted_at',
            'approved_at', 'locked_at', 'clock_events', 'corrections', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_hours', 'overtime_hours', 'created_at', 'updated_at']

    def get_professional_name(self, obj):
        return f"{obj.professional.user.first_name} {obj.professional.user.last_name}"
