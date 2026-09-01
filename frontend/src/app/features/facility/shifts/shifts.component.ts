import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ShiftService } from '../../../core/services/shift.service';
import { FacilityService } from '../../../core/services/facility.service';

@Component({
  selector: 'app-facility-shifts',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight">Shift Planning & Staffing</h2>
        <button (click)="openCreateModal()" class="px-4 py-2 bg-sky-500 hover:bg-sky-600 text-white font-bold rounded-xl text-sm transition shadow-lg shadow-sky-500/20">
          + Create Shift
        </button>
      </div>

      <!-- Shifts Table List -->
      <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
          <span class="font-bold text-slate-800">Available Shift Lists</span>
        </div>
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-100 text-xs font-semibold uppercase text-slate-400 bg-slate-50/20">
              <th class="px-6 py-3">Title / Ward</th>
              <th class="px-6 py-3">Timing</th>
              <th class="px-6 py-3">Workers</th>
              <th class="px-6 py-3">Rate</th>
              <th class="px-6 py-3">Status</th>
              <th class="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm">
            <tr *ngFor="let s of shifts" class="hover:bg-slate-50/30 transition">
              <td class="px-6 py-4">
                <div class="font-bold text-slate-800">{{ s.title }}</div>
                <div class="text-xs text-slate-400">{{ s.facility_name }} • {{ s.ward_name }}</div>
              </td>
              <td class="px-6 py-4">
                <div>{{ s.date }}</div>
                <div class="text-xs text-slate-400">{{ s.start_time }} - {{ s.end_time }}</div>
              </td>
              <td class="px-6 py-4">{{ s.required_workers }}</td>
              <td class="px-6 py-4">€{{ s.pay_rate }}/hr</td>
              <td class="px-6 py-4">
                <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                  [ngClass]="{
                    'bg-teal-100 text-teal-800': s.status === 'FILLED',
                    'bg-sky-100 text-sky-800': s.status === 'POSTED',
                    'bg-amber-100 text-amber-800': s.status === 'DRAFT'
                  }">
                  {{ s.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <button *ngIf="s.status === 'DRAFT'" (click)="publishShift(s.id)" class="px-2.5 py-1 bg-sky-50 hover:bg-sky-100 text-sky-600 font-semibold text-xs rounded-lg transition">
                  Publish
                </button>
              </td>
            </tr>
            <tr *ngIf="shifts.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-slate-400">No shifts created yet.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create Shift Modal -->
      <div *ngIf="showModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white border border-slate-200 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-lg font-bold text-slate-800">Create Staffing Shift</h3>
            <button (click)="closeCreateModal()" class="text-slate-400 hover:text-slate-600 font-bold text-xl leading-none">×</button>
          </div>

          <!-- Alert Messages -->
          <div *ngIf="errorMessage" class="p-3 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs flex items-start gap-2">
            <span class="font-bold">⚠️</span>
            <div class="whitespace-pre-line flex-1">{{ errorMessage }}</div>
          </div>

          <div *ngIf="successMessage" class="p-3 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-xl text-xs flex items-center gap-2">
            <span class="font-bold">✓</span>
            <span class="flex-1">{{ successMessage }}</span>
          </div>

          <form [formGroup]="shiftForm" (ngSubmit)="onCreateSubmit()" class="space-y-4 text-sm">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Facility *</label>
                <select formControlName="facility" (change)="onFacilityChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option value="" disabled selected>-- Select Facility --</option>
                  <option *ngFor="let facility of facilities" [value]="facility.id">
                    {{ facility.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Department *</label>
                <select formControlName="department" (change)="onDepartmentChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option value="" disabled selected>-- Select Department --</option>
                  <option *ngFor="let department of departments" [value]="department.id">
                    {{ department.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Ward *</label>
                <select formControlName="ward" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option value="" disabled selected>-- Select Ward --</option>
                  <option *ngFor="let ward of wards" [value]="ward.id">
                    {{ ward.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Role *</label>
                <select formControlName="role" (change)="onRoleChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option value="" disabled selected>-- Select Role --</option>
                  <option *ngFor="let role of roles" [value]="role.id">
                    {{ role.name }}
                  </option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Specialty *</label>
                <select formControlName="specialty" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option value="" disabled selected>-- Select Specialty --</option>
                  <option *ngFor="let specialty of specialties" [value]="specialty.id">
                    {{ specialty.name }}
                  </option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Title *</label>
                <input type="text" formControlName="title" placeholder="e.g. Registered Nurse Night Shift" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Date *</label>
                <input type="date" formControlName="date" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Start Time *</label>
                <input type="time" formControlName="start_time" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">End Time *</label>
                <input type="time" formControlName="end_time" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Required Workers *</label>
                <input type="number" formControlName="required_workers" min="1" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Pay Rate (€/hr) *</label>
                <input type="number" formControlName="pay_rate" min="10" step="0.5" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Incentive (€)</label>
                <input type="number" formControlName="incentive" min="0" step="1" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="flex justify-end gap-3 border-t border-slate-100 pt-3">
              <button type="button" (click)="closeCreateModal()" [disabled]="isSubmitting" class="px-4 py-2 border border-slate-200 rounded-xl hover:bg-slate-50 disabled:opacity-50">
                Cancel
              </button>
              <button type="submit" [disabled]="shiftForm.invalid || isSubmitting" class="px-4 py-2 bg-sky-500 text-white font-bold rounded-xl hover:bg-sky-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                <span *ngIf="isSubmitting" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>{{ isSubmitting ? 'Saving Shift...' : 'Save Shift' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  `
})
export class FacilityShiftsComponent implements OnInit {
  fb = inject(FormBuilder);
  shiftService = inject(ShiftService);
  facilityService = inject(FacilityService);

  shifts: any[] = [];
  facilities: any[] = [];
  departments: any[] = [];
  wards: any[] = [];
  roles: any[] = [];
  specialties: any[] = [];

  showModal = false;
  isSubmitting = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  shiftForm = this.fb.group({
    facility: ['', Validators.required],
    department: ['', Validators.required],
    ward: ['', Validators.required],
    role: ['', Validators.required],
    specialty: ['', Validators.required],
    title: ['', Validators.required],
    date: ['', Validators.required],
    start_time: ['08:00', Validators.required],
    end_time: ['16:00', Validators.required],
    required_workers: [1, [Validators.required, Validators.min(1)]],
    pay_rate: [35, [Validators.required, Validators.min(10)]],
    incentive: [0]
  });

  ngOnInit() {
    this.loadShifts();
    this.loadDropdownData();
  }

  loadShifts() {
    this.shiftService.getShifts().subscribe({
      next: (res: any) => {
        this.shifts = res?.results ? res.results : (Array.isArray(res) ? res : []);
      },
      error: (err) => {
        console.error('Failed to load shifts:', err);
      }
    });
  }

  loadDropdownData() {
    this.facilityService.getFacilities().subscribe({
      next: (response: any) => {
        console.log('FACILITIES RESPONSE', response);
        this.facilities = response?.results ? response.results : (Array.isArray(response) ? response : []);
        console.log('FACILITIES ARRAY', this.facilities);
      },
      error: (err) => {
        console.error('Failed to load facilities:', err);
      }
    });

    this.facilityService.getRoles().subscribe({
      next: (response: any) => {
        console.log('ROLES RESPONSE', response);
        this.roles = response?.results ? response.results : (Array.isArray(response) ? response : []);
        console.log('ROLES', this.roles);
      },
      error: (err) => {
        console.error('Failed to load roles:', err);
      }
    });
  }

  onFacilityChange() {
    const facilityId = Number(this.shiftForm.get('facility')?.value);
    console.log('SELECTED FACILITY', facilityId);
    this.departments = [];
    this.wards = [];
    this.shiftForm.patchValue({ department: '', ward: '' });

    if (!facilityId) return;

    const selectedFacility = this.facilities.find(f => Number(f.id) === facilityId);
    if (selectedFacility && selectedFacility.departments && selectedFacility.departments.length > 0) {
      this.departments = selectedFacility.departments;
      console.log('DEPARTMENTS', this.departments);
    } else {
      this.facilityService.getDepartments(facilityId).subscribe({
        next: (res: any) => {
          this.departments = res?.results ? res.results : (Array.isArray(res) ? res : []);
          console.log('DEPARTMENTS', this.departments);
        },
        error: (err) => console.error('Failed to load departments:', err)
      });
    }
  }

  onDepartmentChange() {
    const departmentId = Number(this.shiftForm.get('department')?.value);
    console.log('SELECTED DEPARTMENT', departmentId);
    this.wards = [];
    this.shiftForm.patchValue({ ward: '' });

    if (!departmentId) return;

    const selectedDepartment = this.departments.find(d => Number(d.id) === departmentId);
    if (selectedDepartment && selectedDepartment.wards && selectedDepartment.wards.length > 0) {
      this.wards = selectedDepartment.wards;
      console.log('WARDS', this.wards);
    } else {
      this.facilityService.getWards(departmentId).subscribe({
        next: (res: any) => {
          this.wards = res?.results ? res.results : (Array.isArray(res) ? res : []);
          console.log('WARDS', this.wards);
        },
        error: (err) => console.error('Failed to load wards:', err)
      });
    }
  }

  onRoleChange() {
    const roleId = Number(this.shiftForm.get('role')?.value);
    console.log('SELECTED ROLE', roleId);
    this.specialties = [];
    this.shiftForm.patchValue({ specialty: '' });

    if (!roleId) return;

    const selectedRole = this.roles.find(r => Number(r.id) === roleId);
    if (selectedRole && selectedRole.specialties && selectedRole.specialties.length > 0) {
      this.specialties = selectedRole.specialties;
      console.log('SPECIALTIES', this.specialties);
    } else {
      this.facilityService.getSpecialties(roleId).subscribe({
        next: (res: any) => {
          this.specialties = res?.results ? res.results : (Array.isArray(res) ? res : []);
          console.log('SPECIALTIES', this.specialties);
        },
        error: (err) => console.error('Failed to load specialties:', err)
      });
    }
  }

  openCreateModal() {
    this.errorMessage = null;
    this.successMessage = null;
    this.showModal = true;

    // Reset form without pre-selecting options so user can select manually
    this.shiftForm.reset({
      facility: '',
      department: '',
      ward: '',
      role: '',
      specialty: '',
      title: '',
      date: new Date().toISOString().split('T')[0],
      start_time: '08:00',
      end_time: '16:00',
      required_workers: 1,
      pay_rate: 35,
      incentive: 0
    });

    this.departments = [];
    this.wards = [];
    this.specialties = [];

    // Always fetch fresh dropdown data when opening modal
    this.loadDropdownData();
  }

  closeCreateModal() {
    this.showModal = false;
    this.errorMessage = null;
    this.successMessage = null;
    this.isSubmitting = false;
  }

  formatDate(val: any): string {
    if (!val) return '';
    if (val instanceof Date) {
      const y = val.getFullYear();
      const m = String(val.getMonth() + 1).padStart(2, '0');
      const d = String(val.getDate()).padStart(2, '0');
      return `${y}-${m}-${d}`;
    }
    const str = String(val).trim();
    if (str.includes('T')) {
      return str.split('T')[0];
    }
    const dmyMatch = str.match(/^(\d{1,2})[-\/](\d{1,2})[-\/](\d{4})$/);
    if (dmyMatch) {
      const [, d, m, y] = dmyMatch;
      return `${y}-${m.padStart(2, '0')}-${d.padStart(2, '0')}`;
    }
    return str;
  }

  formatTime(val: any): string {
    if (!val) return '08:00:00';
    const str = String(val).trim();
    if (/^\d{1,2}:\d{2}$/.test(str)) {
      const [h, m] = str.split(':');
      return `${h.padStart(2, '0')}:${m}:00`;
    }
    if (/^\d{1,2}:\d{2}:\d{2}$/.test(str)) {
      const [h, m, s] = str.split(':');
      return `${h.padStart(2, '0')}:${m}:${s}`;
    }
    return str;
  }

  onCreateSubmit() {
    this.errorMessage = null;
    this.successMessage = null;

    if (this.shiftForm.invalid) {
      this.shiftForm.markAllAsTouched();
      const invalidControls: string[] = [];
      Object.keys(this.shiftForm.controls).forEach(key => {
        if (this.shiftForm.get(key)?.invalid) {
          invalidControls.push(key);
        }
      });
      this.errorMessage = `Please complete all required fields: ${invalidControls.join(', ')}`;
      return;
    }

    const raw = this.shiftForm.value;
    const facilityId = Number(raw.facility);
    const departmentId = Number(raw.department);
    const wardId = Number(raw.ward);
    const roleId = Number(raw.role);
    const specialtyId = Number(raw.specialty);

    if (!facilityId || !departmentId || !wardId || !roleId || !specialtyId) {
      this.errorMessage = 'Please ensure Facility, Department, Ward, Role, and Specialty are all selected.';
      return;
    }

    const payload = {
      facility: facilityId,
      department: departmentId,
      ward: wardId,
      role: roleId,
      specialty: specialtyId,
      title: (raw.title || '').trim(),
      date: this.formatDate(raw.date),
      start_time: this.formatTime(raw.start_time),
      end_time: this.formatTime(raw.end_time),
      required_workers: Number(raw.required_workers) || 1,
      pay_rate: Number(raw.pay_rate) || 0,
      incentive: Number(raw.incentive) || 0
    };

    this.isSubmitting = true;
    console.log('Sending Create Shift Payload:', payload);

    this.shiftService.createShift(payload).subscribe({
      next: (createdShift) => {
        this.isSubmitting = false;
        this.successMessage = 'Shift created successfully!';
        console.log('Shift created successfully:', createdShift);
        this.loadShifts();
        setTimeout(() => {
          this.closeCreateModal();
        }, 600);
      },
      error: (err) => {
        this.isSubmitting = false;
        console.error('Create Shift API Error:', {
          status: err.status,
          statusText: err.statusText,
          url: err.url,
          error: err.error,
          message: err.message
        });

        let msg = 'Failed to create shift.';
        if (err.status === 401) {
          msg = 'Authentication error (401): Session expired or unauthorized. Please log in again.';
        } else if (err.status === 403) {
          msg = 'Permission denied (403): You do not have permission to create shifts.';
        } else if (err.status === 0) {
          msg = 'Network / CORS error: Unable to reach backend API.';
        } else if (err.error) {
          if (typeof err.error === 'string') {
            msg = err.error;
          } else if (typeof err.error === 'object') {
            const fieldErrors = Object.entries(err.error)
              .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
              .join('\n');
            msg = fieldErrors || JSON.stringify(err.error);
          }
        }
        this.errorMessage = msg;
      }
    });
  }

  publishShift(id: number) {
    this.shiftService.publishShift(id).subscribe({
      next: () => {
        this.loadShifts();
      },
      error: (err) => {
        console.error('Failed to publish shift:', err);
        alert(err?.error?.message || 'Failed to publish shift.');
      }
    });
  }
}
