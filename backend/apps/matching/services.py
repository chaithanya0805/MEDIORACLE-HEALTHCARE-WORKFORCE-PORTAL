from apps.shifts.models import Shift, ShiftBooking, BookingStatus
from apps.professionals.models import ProfessionalProfile
from django.db.models import Q

class MatchingService:
    @staticmethod
    def calculate_match(professional: ProfessionalProfile, shift: Shift):
        explanation = []
        warnings = []
        
        # 1. Qualifications (20%)
        qualification_score = 0
        has_qual = professional.qualifications.filter(status='ACTIVE').exists()
        # For simplicity, if they have active qualifications, we check if they match.
        # Let's say if they have at least one active qualification, we award full 20%.
        if has_qual:
            qualification_score = 20
            explanation.append("✓ Active qualifications verified (20/20)")
        else:
            warnings.append("⚠ No active qualifications found on profile")
            explanation.append("✗ Missing active qualifications (0/20)")

        # 2. Specialty (15%)
        specialty_score = 0
        if professional.specialty == shift.specialty:
            specialty_score = 15
            explanation.append("✓ Specialty matches shift requirement (15/15)")
        else:
            explanation.append(f"✗ Specialty mismatch: profile is {professional.specialty.name if professional.specialty else 'None'}, shift requires {shift.specialty.name} (0/15)")

        # 3. Availability (15%)
        availability_score = 0
        # Check availability status and overlaps
        if professional.availability_status == 'AVAILABLE':
            # Check if there is an overlapping confirmed booking
            overlap = ShiftBooking.objects.filter(
                professional=professional,
                status=BookingStatus.CONFIRMED,
                shift__date=shift.date
            ).exists() # simple date check for overlap in demo
            
            if not overlap:
                availability_score = 15
                explanation.append("✓ Availability status is Available and no conflicts (15/15)")
            else:
                warnings.append("⚠ Overlapping booking on same day")
                explanation.append("✗ Conflicting bookings on this date (0/15)")
        else:
            explanation.append(f"✗ Profile availability is {professional.availability_status} (0/15)")

        # 4. Distance (10%)
        distance_score = 0
        # For demo, let's assign a mock distance based on location matching.
        # If city matches, distance is 10km, else 45km.
        distance = 10 if professional.location.lower() == shift.facility.city.lower() else 45
        if professional.preferred_commute_distance >= distance:
            distance_score = 10
            explanation.append(f"✓ Location is within commute limit ({distance}km vs Max {professional.preferred_commute_distance}km) (10/10)")
        else:
            warnings.append(f"⚠ Commute distance ({distance}km) exceeds preference ({professional.preferred_commute_distance}km)")
            explanation.append(f"✗ Commute distance too far (0/10)")

        # 5. Facility Experience (10%)
        experience_score = 0
        # Check work history or previous bookings completed at the same facility
        had_history = professional.work_histories.filter(facility_name=shift.facility.name).exists()
        had_bookings = ShiftBooking.objects.filter(
            professional=professional,
            shift__facility=shift.facility,
            status=BookingStatus.COMPLETED
        ).exists()
        
        if had_history or had_bookings:
            experience_score = 10
            explanation.append("✓ Previous experience working at this facility (10/10)")
        else:
            experience_score = 0
            explanation.append("✗ No previous recorded experience at this facility (0/10)")

        # 6. Performance (10%)
        # Scale performance_score (which is 0-100) to 10 max
        perf = float(professional.performance_score or 100.0)
        performance_score = round((perf / 100.0) * 10.0, 1)
        explanation.append(f"✓ Performance score is {perf}% ({performance_score}/10)")

        # 7. Reliability (10%)
        # Scale reliability_score (which is 0-100) to 10 max
        rel = float(professional.reliability_score or 100.0)
        reliability_score = round((rel / 100.0) * 10.0, 1)
        explanation.append(f"✓ Reliability rating is {rel}% ({reliability_score}/10)")

        # 8. Rate Compatibility (5%)
        rate_score = 0
        if shift.pay_rate >= professional.minimum_rate:
            if shift.pay_rate >= professional.preferred_rate:
                rate_score = 5
                explanation.append(f"✓ Shift pay rate exceeds preferred rate (€{shift.pay_rate}/hr vs €{professional.preferred_rate}/hr) (5/5)")
            else:
                rate_score = 3
                warnings.append(f"⚠ Pay rate is below preferred rate (€{professional.preferred_rate}) but above minimum rate (€{professional.minimum_rate})")
                explanation.append(f"✓ Pay rate meets minimum requirements (3/5)")
        else:
            warnings.append(f"⚠ Pay rate (€{shift.pay_rate}) is below minimum rate preference (€{professional.minimum_rate})")
            explanation.append("✗ Rate incompatibility (0/5)")

        # 9. Preferences (5%)
        preference_score = 0
        # Check if the facility is preferred M2M
        is_pref_facility = professional.preferred_facilities.filter(id=shift.facility.id).exists()
        if is_pref_facility:
            preference_score = 5
            explanation.append("✓ Facility is in professional's preferred list (5/5)")
        else:
            # check preferred shift types
            pref = getattr(professional, 'preferences', None)
            # Default to day shift preference
            pref_shift_types = pref.preferred_shift_types.split(',') if pref else ['DAY', 'NIGHT', 'EVENING']
            
            # Simple check: shift start hour
            start_hour = shift.start_time.hour
            shift_type = 'DAY'
            if start_hour >= 18 or start_hour < 6:
                shift_type = 'NIGHT'
            elif start_hour >= 12:
                shift_type = 'EVENING'

            if shift_type in pref_shift_types:
                preference_score = 4
                explanation.append(f"✓ Shift type ({shift_type}) matches preferences (4/5)")
            else:
                explanation.append(f"✗ Shift timing does not match profile preferences (0/5)")

        total_score = round(
            qualification_score + specialty_score + availability_score +
            distance_score + experience_score + performance_score +
            reliability_score + rate_score + preference_score, 1
        )

        return {
            "total_score": min(total_score, 100),
            "qualification_score": qualification_score,
            "specialty_score": specialty_score,
            "availability_score": availability_score,
            "distance_score": distance_score,
            "experience_score": experience_score,
            "performance_score": performance_score,
            "reliability_score": reliability_score,
            "rate_score": rate_score,
            "preference_score": preference_score,
            "explanation": explanation,
            "warnings": warnings
        }
