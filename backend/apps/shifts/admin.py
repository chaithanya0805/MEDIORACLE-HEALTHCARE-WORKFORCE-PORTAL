from django.contrib import admin
from apps.shifts.models import Shift, ShiftApplication, ShiftOffer, ShiftBooking

admin.site.register(Shift)
admin.site.register(ShiftApplication)
admin.site.register(ShiftOffer)
admin.site.register(ShiftBooking)
