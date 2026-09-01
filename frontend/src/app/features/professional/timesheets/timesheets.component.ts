import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TimekeepingService } from '../../../core/services/timekeeping.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-professional-timesheets',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">My Timesheets & Timekeeping</h2>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Timesheet List -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <span class="font-bold text-slate-800">Assigned Shift Timesheets</span>
          </div>
          <div class="divide-y divide-slate-100">
            <div *ngFor="let t of timesheets" class="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/30 transition">
              <div>
                <div class="font-bold text-slate-800 text-sm">{{ t.shift_details.title }}</div>
                <div class="text-xs text-slate-400 mt-0.5">
                  {{ t.shift_details.facility_name }} • {{ t.shift_details.date }}
                </div>
                <div class="text-xs font-semibold text-slate-500 mt-2">
                  Hours: {{ t.total_hours || '0.00' }} hrs (Break: {{ t.break_minutes }}m)
                </div>
              </div>
              
              <div class="flex items-center gap-3">
                <span class="px-2.5 py-1 rounded-full text-xs font-semibold"
                  [ngClass]="{
                    'bg-teal-100 text-teal-800': t.status === 'LOCKED',
                    'bg-sky-100 text-sky-800': t.status === 'SUBMITTED',
                    'bg-amber-100 text-amber-800': t.status === 'DRAFT'
                  }">
                  {{ t.status }}
                </span>
                <button (click)="selectTimesheet(t)" class="px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-600 font-semibold text-xs rounded-xl transition">
                  Manage Timeclock
                </button>
              </div>
            </div>
            <div *ngIf="timesheets.length === 0" class="p-6 text-center text-slate-400">
              No timesheets generated yet. Timesheets are automatically created when a shift placement is confirmed.
            </div>
          </div>
        </div>

        <!-- Clock Panel -->
        <div class="space-y-6">
          <div *ngIf="selected" class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 class="font-bold text-slate-800">Clocking Dashboard</h3>
              <button (click)="selected = null" class="text-slate-400 hover:text-slate-600">×</button>
            </div>

            <div class="bg-slate-50 p-4 rounded-xl text-center space-y-2">
              <div class="text-xs text-slate-400 font-semibold uppercase tracking-wider">Clock Status</div>
              <div class="text-base font-bold text-slate-700">
                {{ getClockStatusText() }}
              </div>
            </div>

            <!-- Error and Success Banners -->
            <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-3 rounded-xl text-xs">
              {{ errorMessage }}
            </div>
            <div *ngIf="successMessage" class="bg-teal-500/10 border border-teal-500/20 text-teal-600 p-3 rounded-xl text-xs">
              {{ successMessage }}
            </div>

            <!-- Timeclock Action Buttons -->
            <div *ngIf="selected.status === 'DRAFT'" class="grid grid-cols-2 gap-2 text-xs">
              <button (click)="triggerClockAction('clock_in')" [disabled]="selected.clock_in"
                class="py-2 px-3 bg-sky-500 hover:bg-sky-600 disabled:opacity-40 text-white font-bold rounded-xl transition shadow">
                Clock In
              </button>
              <button (click)="triggerClockAction('clock_out')" [disabled]="!selected.clock_in || selected.clock_out"
                class="py-2 px-3 bg-rose-500 hover:bg-rose-600 disabled:opacity-40 text-white font-bold rounded-xl transition shadow">
                Clock Out
              </button>
              <button (click)="triggerClockAction('break_start')" [disabled]="!selected.clock_in || selected.clock_out"
                class="py-2 px-3 bg-amber-500 hover:bg-amber-600 disabled:opacity-40 text-white font-bold rounded-xl transition shadow">
                Start Break
              </button>
              <button (click)="triggerClockAction('break_end')" [disabled]="!selected.clock_in || selected.clock_out"
                class="py-2 px-3 bg-teal-500 hover:bg-teal-600 disabled:opacity-40 text-white font-bold rounded-xl transition shadow">
                End Break
              </button>
            </div>

            <!-- Signature and Submit -->
            <div *ngIf="selected.status === 'DRAFT' && selected.clock_out" class="border-t border-slate-100 pt-4 space-y-3">
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Professional Signature</label>
              <input type="text" [(ngModel)]="signature" placeholder="Sign your full name..."
                class="w-full text-xs p-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500">
              
              <button (click)="submitTimesheet()" [disabled]="!signature"
                class="w-full py-2 bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs rounded-xl shadow transition">
                Submit Timesheet
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class ProfessionalTimesheetsComponent implements OnInit {
  timekeepingService = inject(TimekeepingService);

  timesheets: any[] = [];
  selected: any = null;
  signature = '';
  errorMessage = '';
  successMessage = '';

  ngOnInit() {
    this.loadTimesheets();
  }

  loadTimesheets() {
    this.timekeepingService.getTimesheets().subscribe({
      next: (res) => this.timesheets = res.results
    });
  }

  selectTimesheet(t: any) {
    this.selected = t;
    this.signature = '';
    this.errorMessage = '';
    this.successMessage = '';
  }

  getClockStatusText(): string {
    if (!this.selected) return 'Inactive';
    if (!this.selected.clock_in) return 'Not Clocked In';
    if (!this.selected.clock_out) return 'Active Shift';
    return 'Completed (Pending Submission)';
  }

  triggerClockAction(action: 'clock_in' | 'clock_out' | 'break_start' | 'break_end') {
    if (!this.selected) return;
    this.errorMessage = '';
    this.successMessage = '';

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const lat = pos.coords.latitude;
        const lng = pos.coords.longitude;
        this.executeClockRequest(action, lat, lng);
      },
      () => {
        // Fallback for demo: pass mock coordinates
        this.executeClockRequest(action, 53.3498, -6.2603);
      }
    );
  }

  executeClockRequest(action: string, lat: number, lng: number) {
    const id = this.selected.id;
    let obs$;
    if (action === 'clock_in') obs$ = this.timekeepingService.clockIn(id, lat, lng);
    else if (action === 'clock_out') obs$ = this.timekeepingService.clockOut(id, lat, lng);
    else if (action === 'break_start') obs$ = this.timekeepingService.breakStart(id, lat, lng);
    else obs$ = this.timekeepingService.breakEnd(id, lat, lng);

    obs$.subscribe({
      next: (res) => {
        this.successMessage = res.message || 'Action executed successfully!';
        this.timekeepingService.getTimesheet(id).subscribe(t => {
          this.selected = t;
          this.loadTimesheets();
        });
      },
      error: (err) => {
        this.errorMessage = err.error?.message || 'Verification failed. GPS location is outside the facility boundary.';
      }
    });
  }

  submitTimesheet() {
    if (!this.selected || !this.signature) return;
    this.timekeepingService.submitTimesheet(this.selected.id, this.signature).subscribe({
      next: () => {
        this.selected = null;
        this.loadTimesheets();
      }
    });
  }
}
