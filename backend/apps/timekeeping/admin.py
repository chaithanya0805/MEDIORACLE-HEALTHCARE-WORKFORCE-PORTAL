from django.contrib import admin
from apps.timekeeping.models import Timesheet, ClockEvent, TimesheetCorrection

admin.site.register(Timesheet)
admin.site.register(ClockEvent)
admin.site.register(TimesheetCorrection)
