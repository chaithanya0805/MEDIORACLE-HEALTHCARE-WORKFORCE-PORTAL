import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ShiftService } from '../../../core/services/shift.service';
import { ProfessionalService } from '../../../core/services/professional.service';

@Component({
  selector: 'app-professional-dashboard',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="space-y-6 font-sans">
      <!-- Expiry Warnings -->
      <div *ngFor="let alert of warnings" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-2xl flex items-center justify-between">
        <div class="flex items-center gap-3 text-sm">
          <svg class="w-5 h-5 shrink-0 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <div>
            <span class="font-bold font-sans">Credential Warning:</span> {{ alert.message }}
          </div>
        </div>
        <a routerLink="../credentials" class="text-xs font-semibold text-rose-400 hover:text-rose-300 bg-rose-500/10 px-3 py-1.5 rounded-xl border border-rose-500/20 transition">
          Renew Now
        </a>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Booked Shifts</div>
          <div class="text-3xl font-extrabold text-slate-800 mt-2">{{ stats?.upcoming_shifts || 0 }}</div>
          <div class="text-xs text-slate-400 mt-1">Confirmed upcoming schedules</div>
        </div>
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Earnings</div>
          <div class="text-3xl font-extrabold text-teal-600 mt-2">€{{ stats?.earnings || 0 | number:'1.2-2' }}</div>
          <div class="text-xs text-slate-400 mt-1">Processed timesheets</div>
        </div>
        <div class="bg-white border border-slate-200/80 rounded-2xl p-5 shadow-sm">
          <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Reliability Rating</div>
          <div class="text-3xl font-extrabold text-amber-500 mt-2">{{ stats?.reliability || 'N/A' }}</div>
          <div class="text-xs text-slate-400 mt-1">Acceptance & Attendance rating</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Offers panel -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex items-center justify-between">
            <span class="font-bold text-slate-800">Direct Shift Offers</span>
          </div>
          <div class="divide-y divide-slate-100">
            <div *ngFor="let o of offers" class="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/30 transition">
              <div>
                <div class="font-bold text-slate-800 text-sm">{{ o.shift_details.title }}</div>
                <div class="text-xs text-slate-400 mt-0.5">
                  {{ o.shift_details.facility_name }} • {{ o.shift_details.date }} • €{{ o.shift_details.pay_rate }}/hr
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button (click)="acceptOffer(o.id)" class="px-3 py-1.5 bg-teal-500 hover:bg-teal-600 text-white font-bold text-xs rounded-xl shadow transition">
                  Accept
                </button>
                <button (click)="rejectOffer(o.id)" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl transition">
                  Decline
                </button>
              </div>
            </div>
            <div *ngIf="offers.length === 0" class="p-6 text-center text-slate-400 text-sm">
              No direct shift offers available at this time.
            </div>
          </div>
        </div>

        <!-- Schedule / Calendar Quick Action -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 space-y-4">
          <h3 class="font-bold text-slate-800">Quick Clock In</h3>
          <p class="text-xs text-slate-400 leading-relaxed">
            Clock in directly for active shifts. You must allow GPS location access to verify geofence.
          </p>
          <a routerLink="../timesheets" class="w-full block text-center py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-500/10 transition">
            Go to Clock Panel
          </a>
        </div>
      </div>
    </div>
  `
})
export class ProfessionalDashboardComponent implements OnInit {
  shiftService = inject(ShiftService);
  profService = inject(ProfessionalService);

  stats: any = null;
  offers: any[] = [];
  warnings: any[] = [];

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.profService.getCredentialDashboard().subscribe({
      next: (res) => {
        this.warnings = res.warnings;
        this.stats = {
          upcoming_shifts: res.stats?.upcoming_bookings || 0,
          earnings: res.stats?.total_earnings || 0,
          reliability: res.stats?.reliability || '98%'
        };
      }
    });

    this.shiftService.getOffers({ status: 'PENDING' }).subscribe({
      next: (res) => this.offers = res.results
    });
  }

  acceptOffer(id: number) {
    this.shiftService.acceptOffer(id).subscribe({
      next: () => this.loadData()
    });
  }

  rejectOffer(id: number) {
    this.shiftService.rejectOffer(id).subscribe({
      next: () => this.loadData()
    });
  }
}
