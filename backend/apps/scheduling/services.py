from apps.shifts.models import ShiftBooking, BookingStatus
from datetime import datetime, timedelta
from django.db import models

class SchedulingConflictEngine:
    @staticmethod
    def check_conflicts(professional, shift):
        # 1. Overlapping Shift check on the same date
        confirmed_bookings = ShiftBooking.objects.filter(
            professional=professional,
            status=BookingStatus.CONFIRMED,
            shift__date=shift.date
        )

        for booking in confirmed_bookings:
            b_shift = booking.shift
            dummy_date = datetime.today().date()
            start_a = datetime.combine(dummy_date, shift.start_time)
            end_a = datetime.combine(dummy_date, shift.end_time)
            
            if end_a <= start_a:
                end_a += timedelta(days=1)
                
            start_b = datetime.combine(dummy_date, b_shift.start_time)
            end_b = datetime.combine(dummy_date, b_shift.end_time)
            if end_b <= start_b:
                end_b += timedelta(days=1)

            if start_a < end_b and start_b < end_a:
                return {
                    "conflict": True,
                    "type": "TIME_OVERLAP",
                    "message": f"Professional has an overlapping shift: {b_shift.title} ({b_shift.start_time} - {b_shift.end_time})."
                }

        # 2. Consecutive shifts / Rest period check (minimum 11 hours rest required between shifts)
        all_bookings = ShiftBooking.objects.filter(
            professional=professional,
            status=BookingStatus.CONFIRMED,
            shift__date__in=[shift.date - timedelta(days=1), shift.date, shift.date + timedelta(days=1)]
        )

        for booking in all_bookings:
            b_shift = booking.shift
            if b_shift.id == shift.id:
                continue
                
            start_a = datetime.combine(shift.date, shift.start_time)
            end_a = datetime.combine(shift.date, shift.end_time)
            if end_a <= start_a:
                end_a += timedelta(days=1)
                
            start_b = datetime.combine(b_shift.date, b_shift.start_time)
            end_b = datetime.combine(b_shift.date, b_shift.end_time)
            if end_b <= start_b:
                end_b += timedelta(days=1)

            if end_a <= start_b:
                rest = (start_b - end_a).total_seconds() / 3600.0
                if rest < 11.0:
                    return {
                        "conflict": True,
                        "type": "REST_PERIOD",
                        "message": f"Insufficient rest period ({round(rest, 1)} hrs) between shift and {b_shift.title}."
                    }
            elif end_b <= start_a:
                rest = (start_a - end_b).total_seconds() / 3600.0
                if rest < 11.0:
                    return {
                        "conflict": True,
                        "type": "REST_PERIOD",
                        "message": f"Insufficient rest period ({round(rest, 1)} hrs) between {b_shift.title} and shift."
                    }

        # 3. Maximum weekly working hours check (max 48 hours)
        start_week = shift.date - timedelta(days=shift.date.weekday())
        end_week = start_week + timedelta(days=6)
        
        week_bookings = ShiftBooking.objects.filter(
            professional=professional,
            status=BookingStatus.CONFIRMED,
            shift__date__range=[start_week, end_week]
        )
        
        total_hours = 0.0
        for booking in week_bookings:
            b_shift = booking.shift
            s_datetime = datetime.combine(b_shift.date, b_shift.start_time)
            e_datetime = datetime.combine(b_shift.date, b_shift.end_time)
            if e_datetime <= s_datetime:
                e_datetime += timedelta(days=1)
            duration = (e_datetime - s_datetime).total_seconds() / 3600.0
            duration -= (b_shift.break_duration / 60.0)
            total_hours += max(duration, 0.0)

        s_curr = datetime.combine(shift.date, shift.start_time)
        e_curr = datetime.combine(shift.date, shift.end_time)
        if e_curr <= s_curr:
            e_curr += timedelta(days=1)
        curr_duration = (e_curr - s_curr).total_seconds() / 3600.0 - (shift.break_duration / 60.0)
        
        if total_hours + curr_duration > 48.0:
            return {
                "conflict": True,
                "type": "MAX_HOURS",
                "message": f"Confirmation would exceed maximum weekly hours (Current: {round(total_hours, 1)} hrs + Shift: {round(curr_duration, 1)} hrs > 48 hrs limit)."
            }

        return {
            "conflict": False,
            "message": "No scheduling conflicts detected."
        }
