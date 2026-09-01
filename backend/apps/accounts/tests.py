from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from apps.accounts.models import Role
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty
from apps.professionals.models import ProfessionalProfile, CredentialType, Credential, CredentialStatus
from apps.compliance.models import ComplianceRule
from apps.compliance.services import ComplianceService
from apps.scheduling.services import SchedulingConflictEngine
from apps.shifts.models import Shift, ShiftStatus, ShiftBooking, BookingStatus
from apps.timekeeping.models import Timesheet, TimesheetStatus
from apps.billing.models import Payment, PaymentStatus

User = get_user_model()

class MediOracleWorkflowTests(TestCase):
    def setUp(self):
        self.facility_admin = User.objects.create_user(
            email='facility@medioracle.com', password='password123', role=Role.FACILITY_ADMIN
        )
        self.compliance_officer = User.objects.create_user(
            email='compliance@medioracle.com', password='password123', role=Role.COMPLIANCE_OFFICER
        )
        self.professional_user = User.objects.create_user(
            email='nurse@medioracle.com', password='password123', role=Role.PROFESSIONAL,
            first_name='Mary', last_name='Jane'
        )

        self.facility = Facility.objects.create(
            name='Mercy Hospital', code='MERCY', facility_type='HOSPITAL',
            address='1 Upper Lane', city='Dublin', state='Leinster', postal_code='D2',
            phone='12345', email='mercy@hospital.ie', contact_person='Manager'
        )
        self.department = Department.objects.create(
            facility=self.facility, name='Emergency', code='MERCY-ER', manager='ER Manager'
        )
        self.ward = Ward.objects.create(
            department=self.department, name='ER Ward 1', code='MERCY-ER-W1',
            capacity=10, required_staff=2, current_staff=1
        )

        self.nurse_role = HealthcareRole.objects.create(name='Registered Nurse')
        self.icu_specialty = Specialty.objects.create(role=self.nurse_role, name='ICU')

        self.profile = ProfessionalProfile.objects.create(
            user=self.professional_user, professional_id='PRO-001', role=self.nurse_role,
            specialty=self.icu_specialty, location='Dublin', email='nurse@medioracle.com',
            phone='12345', preferred_rate=Decimal('45.00'), minimum_rate=Decimal('35.00')
        )

        self.license_type = CredentialType.objects.create(name='Nursing License', code='NMBI')
        self.rule = ComplianceRule.objects.create(
            role=self.nurse_role, credential_type=self.license_type, required=True, minimum_validity_days=30
        )

        self.shift = Shift.objects.create(
            facility=self.facility, department=self.department, ward=self.ward,
            role=self.nurse_role, specialty=self.icu_specialty, title='ICU Night Cover',
            date=date.today() + timedelta(days=2), start_time='20:00:00', end_time='08:00:00',
            required_workers=1, pay_rate=Decimal('45.00'), status=ShiftStatus.POSTED,
            created_by=self.facility_admin
        )

    def test_compliance_engine_fails_when_credential_missing(self):
        compliance = ComplianceService.check_professional_for_shift(self.profile, self.shift)
        self.assertFalse(compliance['eligible'])
        self.assertEqual(len(compliance['missing']), 1)

    def test_compliance_engine_passes_with_verified_credential(self):
        Credential.objects.create(
            professional=self.profile, credential_type=self.license_type, credential_number='12345',
            issuing_authority='NMBI Board', issue_date=date.today() - timedelta(days=10),
            expiry_date=date.today() + timedelta(days=100), verification_status=CredentialStatus.VERIFIED,
            verified_by=self.compliance_officer, verified_at=timezone.now()
        )
        compliance = ComplianceService.check_professional_for_shift(self.profile, self.shift)
        self.assertTrue(compliance['eligible'])
        self.assertEqual(len(compliance['missing']), 0)

    def test_scheduling_conflict_detector(self):
        overlapping_shift = Shift.objects.create(
            facility=self.facility, department=self.department, ward=self.ward,
            role=self.nurse_role, specialty=self.icu_specialty, title='Overlap Day',
            date=self.shift.date, start_time='19:00:00', end_time='23:00:00',
            required_workers=1, pay_rate=Decimal('40.00'), status=ShiftStatus.POSTED
        )
        
        ShiftBooking.objects.create(
            shift=overlapping_shift, professional=self.profile, status=BookingStatus.CONFIRMED,
            confirmed_by=self.facility_admin
        )
        
        conflict = SchedulingConflictEngine.check_conflicts(self.profile, self.shift)
        self.assertTrue(conflict['conflict'])
        self.assertEqual(conflict['type'], 'TIME_OVERLAP')

    def test_duplicate_payment_prevention(self):
        timesheet = Timesheet.objects.create(
            shift=self.shift, professional=self.profile, clock_in=timezone.now(), clock_out=timezone.now() + timedelta(hours=8),
            status=TimesheetStatus.LOCKED
        )
        Payment.objects.create(
            professional=self.profile, timesheet=timesheet, amount=Decimal('320.00'),
            status=PaymentStatus.PAID, reference='REF-1'
        )
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                professional=self.profile, timesheet=timesheet, amount=Decimal('320.00'),
                status=PaymentStatus.PAID, reference='REF-2'
            )
