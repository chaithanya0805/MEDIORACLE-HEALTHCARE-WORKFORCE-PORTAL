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
        <div class="bg-white border border-slate-200 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 class="text-lg font-bold text-slate-800">Create Staffing Shift</h3>
            <button (click)="closeCreateModal()" class="text-slate-400 hover:text-slate-600 font-bold">×</button>
          </div>

          <form [formGroup]="shiftForm" (ngSubmit)="onCreateSubmit()" class="space-y-4 text-sm">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Facility</label>
                <select formControlName="facility" (change)="onFacilityChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option *ngFor="let f of facilities" [value]="f.id">{{ f.name }}</option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Department</label>
                <select formControlName="department" (change)="onDepartmentChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option *ngFor="let d of departments" [value]="d.id">{{ d.name }}</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Ward</label>
                <select formControlName="ward" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option *ngFor="let w of wards" [value]="w.id">{{ w.name }}</option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Role</label>
                <select formControlName="role" (change)="onRoleChange()" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option *ngFor="let r of roles" [value]="r.id">{{ r.name }}</option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Specialty</label>
                <select formControlName="specialty" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
                  <option *ngFor="let sp of specialties" [value]="sp.id">{{ sp.name }}</option>
                </select>
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Title</label>
                <input type="text" formControlName="title" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Date</label>
                <input type="date" formControlName="date" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Start Time</label>
                <input type="time" formControlName="start_time" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">End Time</label>
                <input type="time" formControlName="end_time" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block font-semibold text-slate-700">Required Workers</label>
                <input type="number" formControlName="required_workers" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Pay Rate (€/hr)</label>
                <input type="number" formControlName="pay_rate" required class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
              <div>
                <label class="block font-semibold text-slate-700">Incentive (€)</label>
                <input type="number" formControlName="incentive" class="mt-1 block w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl">
              </div>
            </div>

            <div class="flex justify-end gap-3 border-t border-slate-100 pt-3">
              <button type="button" (click)="closeCreateModal()" class="px-4 py-2 border border-slate-200 rounded-xl hover:bg-slate-50">Cancel</button>
              <button type="submit" [disabled]="shiftForm.invalid" class="px-4 py-2 bg-sky-500 text-white font-bold rounded-xl hover:bg-sky-600">Save Shift</button>
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
  shiftForm = this.fb.group({
    facility: ['', Validators.required],
    department: ['', Validators.required],
    ward: ['', Validators.required],
    role: ['', Validators.required],
    specialty: ['', Validators.required],
    title: ['', Validators.required],
    date: ['', Validators.required],
    start_time: ['', Validators.required],
    end_time: ['', Validators.required],
    required_workers: [1, [Validators.required, Validators.min(1)]],
    pay_rate: ['', [Validators.required, Validators.min(10)]],
    incentive: [0]
  });

  ngOnInit() {
    this.loadShifts();
    this.loadDropdownData();
  }

  loadShifts() {
    this.shiftService.getShifts().subscribe({
      next: (res) => this.shifts = res.results
    });
  }

  loadDropdownData() {
    this.facilityService.getFacilities().subscribe({
      next: (res) => {
        this.facilities = res.results;
        if (this.facilities.length > 0) {
          this.shiftForm.patchValue({ facility: this.facilities[0].id });
          this.onFacilityChange();
        }
      }
    });

    this.facilityService.getRoles().subscribe({
      next: (res) => {
        this.roles = res.results;
        if (this.roles.length > 0) {
          this.shiftForm.patchValue({ role: this.roles[0].id });
          this.onRoleChange();
        }
      }
    });
  }

  onFacilityChange() {
    const fId = Number(this.shiftForm.get('facility')?.value);
    if (!fId) return;
    this.facilityService.getDepartments(fId).subscribe({
      next: (res) => {
        this.departments = res.results;
        if (this.departments.length > 0) {
          this.shiftForm.patchValue({ department: this.departments[0].id });
          this.onDepartmentChange();
        } else {
          this.departments = [];
          this.wards = [];
        }
      }
    });
  }

  onDepartmentChange() {
    const dId = Number(this.shiftForm.get('department')?.value);
    if (!dId) return;
    this.facilityService.getWards(dId).subscribe({
      next: (res) => {
        this.wards = res.results;
        if (this.wards.length > 0) {
          this.shiftForm.patchValue({ ward: this.wards[0].id });
        } else {
          this.wards = [];
        }
      }
    });
  }

  onRoleChange() {
    const rId = Number(this.shiftForm.get('role')?.value);
    if (!rId) return;
    this.facilityService.getSpecialties(rId).subscribe({
      next: (res) => {
        this.specialties = res.results;
        if (this.specialties.length > 0) {
          this.shiftForm.patchValue({ specialty: this.specialties[0].id });
        } else {
          this.specialties = [];
        }
      }
    });
  }

  openCreateModal() {
    this.showModal = true;
  }

  closeCreateModal() {
    this.showModal = false;
  }

  onCreateSubmit() {
    if (this.shiftForm.invalid) return;
    this.shiftService.createShift(this.shiftForm.value).subscribe({
      next: () => {
        this.loadShifts();
        this.closeCreateModal();
      }
    });
  }

  publishShift(id: number) {
    this.shiftService.publishShift(id).subscribe({
      next: () => this.loadShifts()
    });
  }
}
