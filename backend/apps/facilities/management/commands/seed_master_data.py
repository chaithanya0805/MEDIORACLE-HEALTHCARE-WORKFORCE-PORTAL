from django.core.management.base import BaseCommand
from apps.facilities.models import Facility, Department, Ward, HealthcareRole, Specialty, FacilityType, Status

class Command(BaseCommand):
    help = 'Seed real master healthcare options (Facilities, Departments, Wards, Roles, Specialties) using get_or_create'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting healthcare master data seeding...'))

        # 1. Seed Facilities
        facilities_data = [
            {
                'name': 'Apollo Hospital',
                'code': 'APOLLO',
                'facility_type': FacilityType.HOSPITAL,
                'address': 'Jubilee Hills, Road No. 72',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'country': 'India',
                'postal_code': '500033',
                'phone': '+914023607777',
                'email': 'apollo@medioracle.com',
                'contact_person': 'Dr. K. Reddy',
                'budget': 1500000.00,
                'operating_hours': '24/7'
            },
            {
                'name': 'Yashoda Hospital',
                'code': 'YASHODA',
                'facility_type': FacilityType.HOSPITAL,
                'address': 'Raj Bhavan Road, Somajiguda',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'country': 'India',
                'postal_code': '500082',
                'phone': '+914045674567',
                'email': 'yashoda@medioracle.com',
                'contact_person': 'Dr. P. Rao',
                'budget': 1200000.00,
                'operating_hours': '24/7'
            },
            {
                'name': 'KIMS Hospital',
                'code': 'KIMS',
                'facility_type': FacilityType.HOSPITAL,
                'address': '1-8-31/1, Minister Road, Krishna Nagar Colony',
                'city': 'Secunderabad',
                'state': 'Telangana',
                'country': 'India',
                'postal_code': '500003',
                'phone': '+914044885000',
                'email': 'kims@medioracle.com',
                'contact_person': 'Dr. B. Bhaskar Rao',
                'budget': 1000000.00,
                'operating_hours': '24/7'
            }
        ]

        created_facilities = []
        for f_data in facilities_data:
            facility, created = Facility.objects.get_or_create(
                code=f_data['code'],
                defaults=f_data
            )
            created_facilities.append(facility)
            status_text = 'Created' if created else 'Existing'
            self.stdout.write(f"  [{status_text}] Facility: {facility.name} ({facility.code})")

        # 2. Seed Departments and Wards for each Facility
        dept_configs = [
            {
                'name': 'Emergency',
                'code': 'EMERG',
                'manager': 'Dr. A. Sharma (Emergency Lead)',
                'wards': [
                    {'name': 'Emergency Ward', 'code': 'EMERG-W1', 'capacity': 25, 'required_staff': 6}
                ]
            },
            {
                'name': 'ICU',
                'code': 'ICU',
                'manager': 'Dr. S. Nair (Critical Care Lead)',
                'wards': [
                    {'name': 'ICU Ward', 'code': 'ICU-W1', 'capacity': 15, 'required_staff': 8}
                ]
            },
            {
                'name': 'General Medicine',
                'code': 'GENMED',
                'manager': 'Dr. V. Prasad (Chief Medical Officer)',
                'wards': [
                    {'name': 'General Ward', 'code': 'GEN-W1', 'capacity': 40, 'required_staff': 5}
                ]
            },
            {
                'name': 'Cardiology',
                'code': 'CARDIO',
                'manager': 'Dr. R. Gupta (Senior Cardiologist)',
                'wards': [
                    {'name': 'Cardiology Ward', 'code': 'CARD-W1', 'capacity': 20, 'required_staff': 5}
                ]
            },
            {
                'name': 'Pediatrics',
                'code': 'PED',
                'manager': 'Dr. M. Chawla (Pediatrics Head)',
                'wards': [
                    {'name': 'Pediatric Ward', 'code': 'PED-W1', 'capacity': 20, 'required_staff': 4}
                ]
            }
        ]

        for facility in created_facilities:
            self.stdout.write(f"\n  Populating Departments & Wards for {facility.name}...")
            for d_info in dept_configs:
                dept, d_created = Department.objects.get_or_create(
                    facility=facility,
                    code=d_info['code'],
                    defaults={
                        'name': d_info['name'],
                        'manager': d_info['manager'],
                        'status': Status.ACTIVE
                    }
                )
                d_status = 'Created' if d_created else 'Existing'
                self.stdout.write(f"    [{d_status}] Department: {dept.name} ({dept.code})")

                for w_info in d_info['wards']:
                    ward, w_created = Ward.objects.get_or_create(
                        department=dept,
                        code=w_info['code'],
                        defaults={
                            'name': w_info['name'],
                            'capacity': w_info['capacity'],
                            'required_staff': w_info['required_staff'],
                            'current_staff': 0,
                            'status': Status.ACTIVE
                        }
                    )
                    w_status = 'Created' if w_created else 'Existing'
                    self.stdout.write(f"      [{w_status}] Ward: {ward.name} ({ward.code})")

        # 3. Seed Healthcare Roles
        self.stdout.write('\n  Populating Healthcare Roles & Specialties...')
        roles_data = [
            {
                'name': 'Registered Nurse',
                'description': 'Qualified registered nursing professional providing primary and advanced clinical care.'
            },
            {
                'name': 'Staff Nurse',
                'description': 'General ward and unit nursing care specialist for inpatient monitoring.'
            },
            {
                'name': 'Senior Nurse',
                'description': 'Experienced nurse leader overseeing shift workflow, triaging, and quality assurance.'
            },
            {
                'name': 'Healthcare Assistant',
                'description': 'Certified healthcare and nursing aide assisting with patient care, vitals, and mobility.'
            },
            {
                'name': 'Medical Officer',
                'description': 'Attending physician overseeing general diagnostics, rounds, and acute patient care.'
            }
        ]

        specialties_list = [
            {'name': 'Critical Care', 'description': 'Intensive care monitoring, ventilation, and life support.'},
            {'name': 'Emergency Medicine', 'description': 'Rapid triage, trauma management, and resuscitation.'},
            {'name': 'Cardiology', 'description': 'Cardiac diagnostics, ECG telemetry, and coronary care.'},
            {'name': 'Pediatrics', 'description': 'Infant, child, and adolescent healthcare and neonatal support.'},
            {'name': 'General Medicine', 'description': 'Comprehensive adult inpatient and outpatient medical care.'}
        ]

        for r_info in roles_data:
            role, r_created = HealthcareRole.objects.get_or_create(
                name=r_info['name'],
                defaults={'description': r_info['description']}
            )
            r_status = 'Created' if r_created else 'Existing'
            self.stdout.write(f"    [{r_status}] Role: {role.name}")

            # Assign matching specialties for each role
            for sp_info in specialties_list:
                specialty, sp_created = Specialty.objects.get_or_create(
                    role=role,
                    name=sp_info['name'],
                    defaults={'description': sp_info['description']}
                )
                sp_status = 'Created' if sp_created else 'Existing'
                self.stdout.write(f"      [{sp_status}] Specialty: {specialty.name} -> {role.name}")

        self.stdout.write(self.style.SUCCESS('\nSuccessfully seeded all Master Healthcare Data (Facilities, Departments, Wards, Roles, Specialties)!'))
