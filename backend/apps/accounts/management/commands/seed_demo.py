from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import uuid

from apps.accounts.models import Role
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty, Skill, StaffingRequirement
from apps.professionals.models import ProfessionalProfile, CredentialType, Credential, CredentialStatus, Qualification, WorkHistory
from apps.compliance.models import ComplianceRule
from apps.shifts.models import Shift, ShiftStatus, ShiftApplication, ApplicationStatus, ShiftBooking, BookingStatus
from apps.timekeeping.models import Timesheet, TimesheetStatus
from apps.billing.models import Invoice, InvoiceStatus, InvoiceLineItem, Payment, PaymentStatus
from apps.support.models import SupportCase, CaseStatus, CasePriority
from apps.audit.models import AuditEvent
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the MySQL database with complete and realistic demo data.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        # Clear tables in order
        AuditEvent.objects.all().delete()
        SupportCase.objects.all().delete()
        Payment.objects.all().delete()
        Invoice.objects.all().delete()
        Timesheet.objects.all().delete()
        ShiftBooking.objects.all().delete()
        ShiftApplication.objects.all().delete()
        Shift.objects.all().delete()
        ComplianceRule.objects.all().delete()
        Credential.objects.all().delete()
        CredentialType.objects.all().delete()
        ProfessionalProfile.objects.all().delete()
        StaffingRequirement.objects.all().delete()
        Ward.objects.all().delete()
        Department.objects.all().delete()
        Facility.objects.all().delete()
        Specialty.objects.all().delete()
        HealthcareRole.objects.all().delete()
        Skill.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Seeding roles, specialties and skills...')
        
        # Roles
        roles_dict = {}
        for r_name in ['Registered Nurse', 'Healthcare Assistant', 'Pharmacist', 'Technician', 'Midwife', 'Allied Health Professional']:
            roles_dict[r_name] = HealthcareRole.objects.create(name=r_name, description=f"{r_name} general staffing.")

        # Specialties
        spec_dict = {}
        spec_data = {
            'Registered Nurse': ['ICU', 'Emergency', 'Pediatrics', 'Oncology'],
            'Healthcare Assistant': ['General Ward', 'Geriatric Care', 'Mental Health'],
            'Pharmacist': ['Clinical Pharmacy', 'Dispensary'],
            'Technician': ['Radiology', 'Laboratory'],
            'Midwife': ['Labour Ward', 'Postnatal'],
            'Allied Health Professional': ['Physiotherapy', 'Occupational Therapy']
        }
        for role_name, specs in spec_data.items():
            role_obj = roles_dict[role_name]
            for s_name in specs:
                spec_dict[s_name] = Specialty.objects.create(role=role_obj, name=s_name, description=f"{s_name} specialization.")

        # Skills
        skills = ['Phlebotomy', 'Cannulation', 'BLS', 'ACLS', 'Pals', 'Wound Care', 'Patient Handling', 'Triage']
        skill_objs = [Skill.objects.create(name=s) for s in skills]

        # Credential Types
        cred_types = {
            'LICENSE': CredentialType.objects.create(name='Professional License', code='NMBI', description='Nursing/Medical Board registration'),
            'BLS': CredentialType.objects.create(name='Basic Life Support', code='BLS', description='Basic Life Support certification'),
            'ACLS': CredentialType.objects.create(name='Advanced Cardiac Life Support', code='ACLS', description='ACLS certification'),
            'GARDA': CredentialType.objects.create(name='Garda Vetting / Background Check', code='GARDA', description='Police vetting check'),
            'INSURANCE': CredentialType.objects.create(name='Professional Indemnity Insurance', code='INSURANCE', description='Professional liability insurance'),
            'IMMUNIZATION': CredentialType.objects.create(name='Immunization Record', code='IMMUNIZATION', description='Hepatitis B, TB, MMR records'),
            'TRAINING': CredentialType.objects.create(name='Mandatory Training', code='TRAINING', description='Fire safety, infection control, manual handling')
        }

        self.stdout.write('Seeding core demo accounts...')
        common_password = 'password123'

        demo_users_data = [
            ('admin@nexgile.com', Role.SUPER_ADMIN, 'Super', 'Admin'),
            ('facility@nexgile.com', Role.FACILITY_ADMIN, 'Facility', 'Admin'),
            ('professional@nexgile.com', Role.PROFESSIONAL, 'John', 'Professional'),
            ('agency@nexgile.com', Role.RECRUITER, 'Agency', 'Coordinator'),
            ('compliance@nexgile.com', Role.COMPLIANCE_OFFICER, 'Compliance', 'Officer'),
            ('payroll@nexgile.com', Role.PAYROLL_BILLING, 'Payroll', 'Accountant'),
            ('support@nexgile.com', Role.SUPPORT_AGENT, 'Support', 'Agent'),
        ]

        user_objs = {}
        for email, role, f_name, l_name in demo_users_data:
            user = User.objects.create_user(
                email=email,
                password=common_password,
                role=role,
                first_name=f_name,
                last_name=l_name,
                phone='+353871234567'
            )
            user_objs[role] = user

        # Create 5 Facilities
        self.stdout.write('Seeding facilities, departments, and wards...')
        fac_names = [
            ('Beaumont Hospital', 'BEA', 'Dublin 9'),
            ('St. James\'s Hospital', 'SJH', 'Dublin 8'),
            ('Mater Misericordiae', 'MAT', 'Dublin 7'),
            ('Tallaght Hospital', 'TAL', 'Dublin 24'),
            ('University Hospital Galway', 'UHG', 'Galway')
        ]
        
        fac_objs = []
        for name, code, city in fac_names:
            fac = Facility.objects.create(
                name=name,
                code=code,
                facility_type='HOSPITAL',
                address=f'100 Main Street, {city}',
                city=city,
                state='Leinster' if 'Dublin' in city else 'Connacht',
                postal_code='D01' if 'Dublin' in city else 'H91',
                phone='+35312345678',
                email=f'admin@{code.lower()}.ie',
                contact_person='Mr. Operations Manager',
                budget=Decimal('500000.00')
            )
            fac_objs.append(fac)

            # Create Departments for each facility
            dept_names = ['Emergency', 'Intensive Care Unit (ICU)', 'General Medicine']
            for d_idx, d_name in enumerate(dept_names):
                dept = Department.objects.create(
                    facility=fac,
                    name=d_name,
                    code=f"{code}-DEP-{d_idx+1}",
                    manager='Dept Head Manager'
                )
                
                # Create Wards for each Department
                ward_names = ['Ward A', 'Ward B']
                for w_idx, w_name in enumerate(ward_names):
                    Ward.objects.create(
                        department=dept,
                        name=f"{d_name} - {w_name}",
                        code=f"{dept.code}-WD-{w_idx+1}",
                        capacity=25,
                        required_staff=4,
                        current_staff=2
                    )

        # Create Compliance Rules
        self.stdout.write('Seeding compliance rules...')
        nurse_role = roles_dict['Registered Nurse']
        ComplianceRule.objects.create(role=nurse_role, credential_type=cred_types['LICENSE'], required=True, minimum_validity_days=30)
        ComplianceRule.objects.create(role=nurse_role, credential_type=cred_types['BLS'], required=True, minimum_validity_days=15)
        ComplianceRule.objects.create(role=nurse_role, credential_type=cred_types['ACLS'], required=True, minimum_validity_days=15)
        ComplianceRule.objects.create(role=nurse_role, credential_type=cred_types['INSURANCE'], required=True, minimum_validity_days=30)

        hca_role = roles_dict['Healthcare Assistant']
        ComplianceRule.objects.create(role=hca_role, credential_type=cred_types['GARDA'], required=True, minimum_validity_days=30)
        ComplianceRule.objects.create(role=hca_role, credential_type=cred_types['TRAINING'], required=True, minimum_validity_days=15)

        # Create 30 Professionals
        self.stdout.write('Seeding 30 professionals profiles & credentials...')
        for i in range(1, 31):
            p_user = User.objects.create_user(
                email=f"professional{i}@nexgile.com",
                password=common_password,
                role=Role.PROFESSIONAL,
                first_name=f"Professional_{i}",
                last_name=f"Surname_{i}",
                phone=f"+3538700000{i:02d}"
            )
            
            # Alternate roles
            if i % 3 == 0:
                selected_role = roles_dict['Registered Nurse']
                selected_spec = spec_dict['ICU'] if i % 2 == 0 else spec_dict['Emergency']
            elif i % 3 == 1:
                selected_role = roles_dict['Healthcare Assistant']
                selected_spec = spec_dict['General Ward']
            else:
                selected_role = roles_dict['Midwife']
                selected_spec = spec_dict['Labour Ward']

            profile = ProfessionalProfile.objects.create(
                user=p_user,
                professional_id=f"PRO-{i:03d}-DEMO",
                role=selected_role,
                specialty=selected_spec,
                location='Dublin' if i % 2 == 0 else 'Galway',
                address=f"{i * 10} Hospital Lane",
                email=p_user.email,
                phone=p_user.phone,
                years_experience=i % 10 + 2,
                bio=f"Demo profile for qualified professional number {i}.",
                availability_status='AVAILABLE',
                preferred_rate=Decimal('35.00') + Decimal(str(i)),
                minimum_rate=Decimal('30.00'),
                preferred_commute_distance=60,
                rating=Decimal('4.5') + Decimal(str(i % 5)) / Decimal('10.0'),
                reliability_score=Decimal('90.00') + Decimal(str(i % 10)),
                performance_score=Decimal('92.00') + Decimal(str(i % 8))
            )

            # Qualifications
            Qualification.objects.create(
                professional=profile,
                name=f"B.Sc. in Nursing / Healthcare certification {i}",
                issuing_body="Irish Nursing Board / College",
                issue_date=date.today() - timedelta(days=365 * 3),
                expiry_date=date.today() + timedelta(days=365)
            )

            # Work history
            WorkHistory.objects.create(
                professional=profile,
                facility_name="St. Vincent's University Hospital",
                role=selected_role.name,
                start_date=date.today() - timedelta(days=365 * 2),
                end_date=date.today() - timedelta(days=100)
            )

            # Seed mandatory credentials
            # Alternating states: verified, expiring soon, pending
            if selected_role == roles_dict['Registered Nurse']:
                # NMBI License
                Credential.objects.create(
                    professional=profile,
                    credential_type=cred_types['LICENSE'],
                    credential_number=f"NMBI-{10000+i}",
                    issuing_authority="NMBI Ireland",
                    issue_date=date.today() - timedelta(days=100),
                    expiry_date=date.today() + timedelta(days=15 if i % 5 == 0 else 300), # Expiring soon for i % 5 == 0
                    verification_status=CredentialStatus.VERIFIED,
                    verified_by=user_objs[Role.COMPLIANCE_OFFICER],
                    verified_at=timezone.now()
                )
                
                # BLS
                Credential.objects.create(
                    professional=profile,
                    credential_type=cred_types['BLS'],
                    credential_number=f"BLS-{20000+i}",
                    issuing_authority="Irish Heart Association",
                    issue_date=date.today() - timedelta(days=50),
                    expiry_date=date.today() + timedelta(days=10 if i % 4 == 0 else 180), # Expired/Expiring soon for i % 4 == 0
                    verification_status=CredentialStatus.VERIFIED,
                    verified_by=user_objs[Role.COMPLIANCE_OFFICER],
                    verified_at=timezone.now()
                )
                
                # ACLS
                Credential.objects.create(
                    professional=profile,
                    credential_type=cred_types['ACLS'],
                    credential_number=f"ACLS-{30000+i}",
                    issuing_authority="AHA Association",
                    issue_date=date.today() - timedelta(days=80),
                    expiry_date=date.today() + timedelta(days=400),
                    verification_status=CredentialStatus.VERIFIED,
                    verified_by=user_objs[Role.COMPLIANCE_OFFICER],
                    verified_at=timezone.now()
                )
                
                # Insurance
                Credential.objects.create(
                    professional=profile,
                    credential_type=cred_types['INSURANCE'],
                    credential_number=f"INS-{40000+i}",
                    issuing_authority="MedShield Insurance",
                    issue_date=date.today() - timedelta(days=120),
                    expiry_date=date.today() + timedelta(days=200),
                    verification_status=CredentialStatus.VERIFIED,
                    verified_by=user_objs[Role.COMPLIANCE_OFFICER],
                    verified_at=timezone.now()
                )

        # Seeding a demo shifts flow
        self.stdout.write('Seeding demo shifts, applications, and bookings...')
        demo_fac = fac_objs[0] # Beaumont Hospital
        demo_dept = demo_fac.departments.first()
        demo_ward = demo_dept.wards.first()
        demo_role = roles_dict['Registered Nurse']
        demo_spec = spec_dict['ICU']

        # 1. Open shift for professional to apply
        open_shift = Shift.objects.create(
            facility=demo_fac,
            department=demo_dept,
            ward=demo_ward,
            role=demo_role,
            specialty=demo_spec,
            title="Registered Nurse Night Shift ICU",
            description="Night shift ICU nurse support needed due to sudden census spike.",
            date=date.today() + timedelta(days=5),
            start_time="20:00:00",
            end_time="08:00:00",
            location="Building 1, ICU Ward",
            required_workers=2,
            pay_rate=Decimal("45.00"),
            incentive=Decimal("50.00"),
            break_duration=45,
            status=ShiftStatus.POSTED,
            created_by=user_objs[Role.FACILITY_ADMIN]
        )

        # Apply using professional 3 (an RN)
        prof_rn = ProfessionalProfile.objects.filter(role=demo_role).first()
        ShiftApplication.objects.create(
            shift=open_shift,
            professional=prof_rn,
            status=ApplicationStatus.APPLIED
        )

        # 2. Confirmed Booking in progress / finished
        past_shift = Shift.objects.create(
            facility=demo_fac,
            department=demo_dept,
            ward=demo_ward,
            role=demo_role,
            specialty=demo_spec,
            title="Registered Nurse Emergency Day Shift",
            description="Emergency Ward general nurse cover.",
            date=date.today() - timedelta(days=1),
            start_time="08:00:00",
            end_time="16:00:00",
            location="Emergency Entrance",
            required_workers=1,
            pay_rate=Decimal("40.00"),
            incentive=Decimal("0.00"),
            break_duration=30,
            status=ShiftStatus.COMPLETED,
            created_by=user_objs[Role.FACILITY_ADMIN]
        )

        booking = ShiftBooking.objects.create(
            shift=past_shift,
            professional=prof_rn,
            status=BookingStatus.COMPLETED,
            confirmed_by=user_objs[Role.FACILITY_ADMIN],
            compliance_checked_at=timezone.now()
        )

        # Add timesheet, clock-in/out
        timesheet = Timesheet.objects.create(
            shift=past_shift,
            professional=prof_rn,
            clock_in=timezone.make_aware(timezone.datetime.combine(past_shift.date, timezone.datetime.strptime("08:02:00", "%H:%M:%S").time())),
            clock_out=timezone.make_aware(timezone.datetime.combine(past_shift.date, timezone.datetime.strptime("16:04:00", "%H:%M:%S").time())),
            break_minutes=30,
            total_hours=Decimal("7.53"),
            overtime_hours=Decimal("0.00"),
            status=TimesheetStatus.LOCKED,
            submitted_at=timezone.now(),
            approved_at=timezone.now(),
            locked_at=timezone.now(),
            manager_approval=user_objs[Role.FACILITY_ADMIN]
        )

        # Auto invoice & payment
        invoice = Invoice.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            facility=demo_fac,
            shift=past_shift,
            subtotal=Decimal("301.20"),
            tax=Decimal("60.24"),
            total=Decimal("361.44"),
            due_date=date.today() + timedelta(days=30),
            status=InvoiceStatus.ISSUED
        )
        InvoiceLineItem.objects.create(
            invoice=invoice,
            shift=past_shift,
            professional=prof_rn,
            hours=Decimal("7.53"),
            rate=Decimal("40.00"),
            amount=Decimal("301.20")
        )

        Payment.objects.create(
            professional=prof_rn,
            timesheet=timesheet,
            amount=Decimal("301.20"),
            status=PaymentStatus.PAID,
            reference=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            paid_at=timezone.now()
        )

        # 3. Create Support cases
        SupportCase.objects.create(
            case_id=f"CASE-{uuid.uuid4().hex[:8].upper()}",
            user=prof_rn.user,
            facility=demo_fac,
            category='App / GPS Issues',
            priority=CasePriority.HIGH,
            description="My GPS clock-in validation keeps throwing geofence mismatch.",
            status=CaseStatus.OPEN
        )

        # 4. Create Audit Logs
        AuditEvent.objects.create(
            user=user_objs[Role.SUPER_ADMIN],
            action="SYSTEM_INITIALIZE_DEMO",
            reason="Populating database with base testing seed details."
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded all nexgile_db entities!'))
