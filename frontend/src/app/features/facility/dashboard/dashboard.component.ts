import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ShiftService } from '../../../core/services/shift.service';
import { TimekeepingService } from '../../../core/services/timekeeping.service';
import { AnalyticsService } from '../../../core/services/analytics.service';

@Component({
  selector: 'app-facility-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="space-y-6 font-sans">
      <!-- Stats cards grid -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Posted Shifts</div>
          <div class="text-3xl font-extrabold text-slate-800 mt-2">{{ stats?.total_posted || 0 }}</div>
          <div class="text-xs text-slate-400 mt-1">Total shifts listed</div>
        </div>
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Confirmed Bookings</div>
          <div class="text-3xl font-extrabold text-slate-800 mt-2 text-sky-600">{{ stats?.total_confirmed || 0 }}</div>
          <div class="text-xs text-slate-400 mt-1">Filled by professionals</div>
        </div>
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Fill Rate</div>
          <div class="text-3xl font-extrabold mt-2" [ngClass]="stats?.fill_rate >= 80 ? 'text-teal-600' : 'text-amber-500'">
            {{ stats?.fill_rate || 0 }}%
          </div>
          <div class="text-xs text-slate-400 mt-1">Acceptance percentage</div>
        </div>
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Staffing Spend</div>
          <div class="text-3xl font-extrabold text-slate-800 mt-2">€{{ stats?.staffing_spend || 0 | number:'1.2-2' }}</div>
          <div class="text-xs text-slate-400 mt-1">YTD Invoice totals</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Upcoming Shifts -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
            <h3 class="font-bold text-slate-800">Posted Staffing Shifts</h3>
            <a routerLink="../shifts" class="text-xs font-semibold text-sky-500 hover:text-sky-600">Manage all</a>
          </div>
          <div class="divide-y divide-slate-100">
            <div *ngFor="let s of shifts" class="px-6 py-4 flex items-center justify-between hover:bg-slate-50/50 transition">
              <div>
                <div class="font-bold text-slate-800 text-sm">{{ s.title }}</div>
                <div class="text-xs text-slate-400 mt-0.5">
                  {{ s.facility_name }} • {{ s.date }} • {{ s.start_time }} - {{ s.end_time }}
                </div>
              </div>
              <span class="px-2.5 py-1 rounded-full text-xs font-semibold"
                [ngClass]="{
                  'bg-teal-100 text-teal-800': s.status === 'FILLED',
                  'bg-sky-100 text-sky-800': s.status === 'POSTED',
                  'bg-slate-100 text-slate-800': s.status === 'DRAFT'
                }">
                {{ s.status }}
              </span>
            </div>
            <div *ngIf="shifts.length === 0" class="px-6 py-8 text-center text-slate-400 text-sm">
              No shifts posted yet. Click 'Manage Shifts' to create a requirement.
            </div>
          </div>
        </div>

        <!-- Alerts / Shortages & Approvals -->
        <div class="space-y-6">
          <!-- Pending Timesheets -->
          <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6">
            <h3 class="font-bold text-slate-800 mb-4">Pending Approvals</h3>
            <div class="space-y-4">
              <div *ngFor="let t of timesheets" class="flex items-center justify-between border-b border-slate-100 pb-3 last:border-0 last:pb-0">
                <div>
                  <div class="font-semibold text-slate-800 text-sm">{{ t.professional_name }}</div>
                  <div class="text-xs text-slate-400 mt-0.5">{{ t.shift_details.title }} • {{ t.total_hours }} hrs</div>
                </div>
                <a routerLink="../timesheets" class="px-3 py-1 bg-sky-50 hover:bg-sky-100 text-sky-600 font-semibold text-xs rounded-lg transition">
                  Review
                </a>
              </div>
              <div *ngIf="timesheets.length === 0" class="text-center py-4 text-slate-400 text-sm">
                ✓ No pending timesheets to approve
              </div>
            </div>
          </div>

          <!-- Shortage Alert Card -->
          <div *ngIf="stats?.fill_rate < 80" class="bg-amber-500/10 border border-amber-500/20 text-amber-800 rounded-2xl p-6">
            <h4 class="font-bold text-sm text-amber-900 flex items-center gap-2">
              <svg class="w-5 h-5 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              Critical Shortage Alert
            </h4>
            <p class="text-xs text-amber-700 mt-2 leading-relaxed">
              Platform fill-rate is below target ({{ stats?.fill_rate }}%). Create new shifts or trigger match score generation.
            </p>
          </div>
        </div>
      </div>
    </div>
  `
})
export class FacilityDashboardComponent implements OnInit {
  shiftService = inject(ShiftService);
  timekeepingService = inject(TimekeepingService);
  analyticsService = inject(AnalyticsService);

  stats: any = null;
  shifts: any[] = [];
  timesheets: any[] = [];

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.analyticsService.getFacilityAnalytics().subscribe({
      next: (res) => this.stats = res.data
    });

    this.shiftService.getShifts().subscribe({
      next: (res) => this.shifts = res.results.slice(0, 5)
    });

    this.timekeepingService.getTimesheets({ status: 'SUBMITTED' }).subscribe({
      next: (res) => this.timesheets = res.results
    });
  }
}
