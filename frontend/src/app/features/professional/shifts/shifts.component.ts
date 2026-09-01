import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShiftService } from '../../../core/services/shift.service';

@Component({
  selector: 'app-professional-shifts',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Available Care Staffing Shifts</h2>

      <!-- Success / Error Alert banners -->
      <div *ngIf="successMessage" class="bg-teal-500/10 border border-teal-500/20 text-teal-600 p-4 rounded-2xl text-sm font-semibold">
        {{ successMessage }}
      </div>
      <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-2xl text-sm font-semibold">
        {{ errorMessage }}
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div *ngFor="let s of shifts" class="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-sm flex flex-col justify-between space-y-4 hover:shadow-md transition">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-50 text-sky-700">{{ s.role_name }}</span>
              <span class="font-bold text-slate-800 text-sm">€{{ s.pay_rate }}/hr</span>
            </div>
            <div>
              <h3 class="font-bold text-slate-800 text-base">{{ s.title }}</h3>
              <p class="text-xs text-slate-400 mt-0.5">{{ s.facility_name }} • {{ s.ward_name }}</p>
            </div>
            <p class="text-xs text-slate-500 leading-relaxed truncate">{{ s.description }}</p>
            <div class="text-2xs font-semibold text-slate-400 uppercase tracking-wider space-y-1">
              <div>📅 Date: {{ s.date }}</div>
              <div>⏰ Timing: {{ s.start_time }} - {{ s.end_time }} (Break: {{ s.break_duration }}m)</div>
            </div>
          </div>

          <button (click)="apply(s.id)" [disabled]="isApplied(s.id)"
            class="w-full py-2.5 bg-sky-500 hover:bg-sky-600 disabled:bg-slate-100 disabled:text-slate-400 text-white font-bold text-xs rounded-xl shadow transition">
            {{ isApplied(s.id) ? 'Applied' : 'Apply for Shift' }}
          </button>
        </div>

        <div *ngIf="shifts.length === 0" class="col-span-2 py-12 text-center text-slate-400">
          No shifts are currently posted for your role. Please check back later.
        </div>
      </div>
    </div>
  `
})
export class ProfessionalShiftsComponent implements OnInit {
  shiftService = inject(ShiftService);

  shifts: any[] = [];
  appliedShiftIds: number[] = [];
  successMessage = '';
  errorMessage = '';

  ngOnInit() {
    this.loadShifts();
    this.loadApplied();
  }

  loadShifts() {
    this.shiftService.getShifts({ status: 'POSTED' }).subscribe({
      next: (res) => this.shifts = res.results
    });
  }

  loadApplied() {
    this.shiftService.getApplications().subscribe({
      next: (res) => {
        this.appliedShiftIds = res.results.map((app: any) => app.shift);
      }
    });
  }

  isApplied(shiftId: number): boolean {
    return this.appliedShiftIds.includes(shiftId);
  }

  apply(shiftId: number) {
    this.successMessage = '';
    this.errorMessage = '';
    this.shiftService.applyToShift(shiftId).subscribe({
      next: (res) => {
        this.successMessage = res.message || 'Application submitted successfully!';
        this.loadApplied();
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Failed to submit application. Please check compatibilities.';
        console.error('Apply error details:', err);
      }
    });
  }
}
