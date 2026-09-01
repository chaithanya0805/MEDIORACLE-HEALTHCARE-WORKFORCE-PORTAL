import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TimekeepingService } from '../../../core/services/timekeeping.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-facility-timesheets',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Timesheet Verification & Approvals</h2>

      <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <span class="font-bold text-slate-800">Timesheets Submitted</span>
        </div>
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="border-b border-slate-100 text-xs font-semibold uppercase text-slate-400 bg-slate-50/20">
              <th class="px-6 py-3">Professional</th>
              <th class="px-6 py-3">Shift Details</th>
              <th class="px-6 py-3">Hours Logged</th>
              <th class="px-6 py-3">Status</th>
              <th class="px-6 py-3">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-sm">
            <tr *ngFor="let t of timesheets" class="hover:bg-slate-50/30 transition">
              <td class="px-6 py-4 font-bold text-slate-800">{{ t.professional_name }}</td>
              <td class="px-6 py-4">
                <div class="font-medium text-slate-700">{{ t.shift_details.title }}</div>
                <div class="text-xs text-slate-400">{{ t.shift_details.date }} • {{ t.shift_details.start_time }} - {{ t.shift_details.end_time }}</div>
              </td>
              <td class="px-6 py-4">
                <div class="font-bold text-slate-800">{{ t.total_hours }} hrs</div>
                <div class="text-xs text-slate-400">Break: {{ t.break_minutes }} mins • Overtime: {{ t.overtime_hours }} hrs</div>
              </td>
              <td class="px-6 py-4">
                <span class="px-2 py-0.5 rounded-full text-xs font-semibold"
                  [ngClass]="{
                    'bg-teal-100 text-teal-800': t.status === 'LOCKED',
                    'bg-sky-100 text-sky-800': t.status === 'SUBMITTED',
                    'bg-slate-100 text-slate-800': t.status === 'DRAFT'
                  }">
                  {{ t.status }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <button *ngIf="t.status === 'SUBMITTED'" (click)="approveTimesheet(t.id)" class="px-3 py-1 bg-teal-500 hover:bg-teal-600 text-white font-bold text-xs rounded-lg transition">
                    Approve
                  </button>
                  <button *ngIf="t.status === 'SUBMITTED'" (click)="openCorrectModal(t)" class="px-3 py-1 bg-amber-50 hover:bg-amber-100 text-amber-700 font-semibold text-xs rounded-lg transition">
                    Correct
                  </button>
                </div>
              </td>
            </tr>
            <tr *ngIf="timesheets.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-slate-400">No timesheets awaiting approval.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Correction Modal -->
      <div *ngIf="showModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-white border border-slate-200 rounded-2xl max-w-sm w-full p-6 shadow-2xl space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <h3 class="font-bold text-slate-800">Timesheet Correction</h3>
            <button (click)="showModal = false" class="text-slate-400 hover:text-slate-600">×</button>
          </div>
          <div class="space-y-4 text-xs">
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Adjusted Total Hours</label>
              <input type="number" [(ngModel)]="correctedHours" class="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl">
            </div>
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Reason for correction</label>
              <textarea [(ngModel)]="correctionReason" placeholder="Specify details..." class="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl h-20"></textarea>
            </div>
          </div>
          <div class="flex justify-end gap-2 text-xs pt-2">
            <button (click)="showModal = false" class="px-3 py-1.5 border border-slate-200 rounded-lg">Cancel</button>
            <button (click)="submitCorrection()" class="px-3 py-1.5 bg-amber-500 text-white font-bold rounded-lg">Apply Adjustment</button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class FacilityTimesheetsComponent implements OnInit {
  timekeepingService = inject(TimekeepingService);

  timesheets: any[] = [];
  selectedTimesheet: any = null;
  showModal = false;
  correctedHours = 0;
  correctionReason = '';

  ngOnInit() {
    this.loadTimesheets();
  }

  loadTimesheets() {
    this.timekeepingService.getTimesheets().subscribe({
      next: (res) => this.timesheets = res.results
    });
  }

  approveTimesheet(id: number) {
    this.timekeepingService.approveTimesheet(id).subscribe({
      next: () => this.loadTimesheets()
    });
  }

  openCorrectModal(t: any) {
    this.selectedTimesheet = t;
    this.correctedHours = Number(t.total_hours);
    this.correctionReason = '';
    this.showModal = true;
  }

  submitCorrection() {
    if (!this.selectedTimesheet) return;
    this.timekeepingService.correctTimesheet(this.selectedTimesheet.id, this.correctedHours, this.correctionReason).subscribe({
      next: () => {
        this.showModal = false;
        this.loadTimesheets();
      }
    });
  }
}
