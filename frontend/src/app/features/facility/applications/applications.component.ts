import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShiftService } from '../../../core/services/shift.service';
import { MatchingService } from '../../../core/services/matching.service';
import { ComplianceService } from '../../../core/services/compliance.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-facility-applications',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Shift Applications & Placements</h2>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Applications List -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden lg:col-span-2">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
            <span class="font-bold text-slate-800">Pending Applications</span>
          </div>
          <div class="divide-y divide-slate-100">
            <div *ngFor="let app of applications" class="p-6 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:bg-slate-50/30 transition">
              <div>
                <div class="font-bold text-slate-800 text-base">{{ app.professional_name }}</div>
                <div class="text-xs text-slate-400 mt-0.5">ID: {{ app.professional_code }} • Rating: {{ app.rating }}/5.0</div>
                <div class="text-xs font-semibold text-sky-600 mt-2 bg-sky-50 px-2 py-0.5 rounded inline-block">
                  Applied for: {{ app.shift_details.title }}
                </div>
              </div>
              <div class="flex flex-wrap items-center gap-3">
                <button (click)="viewMatchDetails(app)" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-xl transition">
                  Match Score
                </button>
                <button (click)="checkCompliance(app)" class="px-3 py-1.5 bg-sky-50 hover:bg-sky-100 text-sky-600 font-semibold text-xs rounded-xl transition">
                  Verify Compliance
                </button>
                <button *ngIf="app.status === 'APPLIED'" (click)="sendOffer(app)" class="px-3 py-1.5 bg-teal-500 hover:bg-teal-600 text-white font-bold text-xs rounded-xl transition shadow">
                  Send Offer
                </button>
              </div>
            </div>
            <div *ngIf="applications.length === 0" class="p-6 text-center text-slate-400">
              No pending applications found.
            </div>
          </div>
        </div>

        <!-- Details Panel (Dynamic selection of Match or Compliance) -->
        <div class="space-y-6">
          <!-- Match Score Panel -->
          <div *ngIf="selectedMatch" class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 class="font-bold text-slate-800">Match Score Analysis</h3>
              <button (click)="selectedMatch = null" class="text-slate-400 hover:text-slate-600">×</button>
            </div>
            
            <div class="text-center py-4 bg-slate-50 rounded-2xl">
              <div class="text-3xl font-extrabold text-sky-600">{{ selectedMatch.score }}%</div>
              <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mt-1">Total Compatibility</div>
            </div>

            <div class="space-y-2 text-xs">
              <span class="font-bold text-slate-500 uppercase tracking-wider block">Score Details</span>
              <div *ngFor="let expl of selectedMatch.details.explanation" class="text-slate-600 py-1 border-b border-slate-50 last:border-0">
                {{ expl }}
              </div>
            </div>

            <!-- Warnings -->
            <div *ngIf="selectedMatch.details.warnings.length > 0" class="bg-amber-500/10 border border-amber-500/20 text-amber-800 rounded-xl p-3 text-xs space-y-1">
              <span class="font-bold block">Warnings:</span>
              <div *ngFor="let warn of selectedMatch.details.warnings">
                {{ warn }}
              </div>
            </div>
          </div>

          <!-- Compliance Checklist Panel -->
          <div *ngIf="selectedCompliance" class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 space-y-4">
            <div class="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 class="font-bold text-slate-800">Compliance & Verification</h3>
              <button (click)="selectedCompliance = null" class="text-slate-400 hover:text-slate-600">×</button>
            </div>

            <div class="text-center py-3 rounded-2xl" [ngClass]="selectedCompliance.eligible ? 'bg-teal-100 text-teal-800' : 'bg-rose-100 text-rose-800'">
              <span class="font-bold text-sm uppercase tracking-wider">
                {{ selectedCompliance.eligible ? 'COMPLIANT' : 'NOT COMPLIANT' }}
              </span>
            </div>

            <!-- Missing / Expired items -->
            <div class="space-y-3 text-xs">
              <div *ngIf="selectedCompliance.missing.length > 0">
                <span class="font-bold text-rose-600 uppercase tracking-wider block mb-1">Missing Requirements:</span>
                <div *ngFor="let m of selectedCompliance.missing" class="bg-rose-50 border border-rose-100/50 p-2 rounded-xl text-rose-700 flex justify-between">
                  <span>{{ m.credential_type }}</span>
                  <span class="font-semibold">{{ m.status }}</span>
                </div>
              </div>

              <div *ngIf="selectedCompliance.expired.length > 0">
                <span class="font-bold text-rose-600 uppercase tracking-wider block mb-1">Expired Credentials:</span>
                <div *ngFor="let ex of selectedCompliance.expired" class="bg-rose-50 border border-rose-100/50 p-2 rounded-xl text-rose-700">
                  {{ ex.credential_type }} (Expired {{ ex.expired_days_ago }} days ago)
                </div>
              </div>

              <div *ngIf="selectedCompliance.warnings.length > 0">
                <span class="font-bold text-amber-600 uppercase tracking-wider block mb-1">Compliance Warnings:</span>
                <div *ngFor="let w of selectedCompliance.warnings" class="bg-amber-50 border border-amber-100/50 p-2 rounded-xl text-amber-700">
                  {{ w }}
                </div>
              </div>

              <div *ngIf="selectedCompliance.missing.length === 0 && selectedCompliance.expired.length === 0" class="text-teal-600 font-semibold flex items-center gap-1">
                ✓ All required credentials are active and verified.
              </div>
            </div>

            <!-- Compliance Override section -->
            <div *ngIf="!selectedCompliance.eligible" class="border-t border-slate-100 pt-3 space-y-2">
              <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider">Authorized Compliance Override</label>
              <textarea [(ngModel)]="overrideReason" placeholder="Enter reason for override..."
                class="w-full text-xs p-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500"></textarea>
            </div>

            <!-- Confirm Booking Trigger -->
            <button (click)="confirmBooking()"
              class="w-full py-2 bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs rounded-xl transition shadow">
              Confirm Booking Placement
            </button>
            <div *ngIf="bookingError" class="text-xs text-rose-600 font-semibold mt-2">{{ bookingError }}</div>
            <div *ngIf="bookingSuccess" class="text-xs text-teal-600 font-semibold mt-2">✓ Booking confirmed successfully!</div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class FacilityApplicationsComponent implements OnInit {
  shiftService = inject(ShiftService);
  matchingService = inject(MatchingService);
  complianceService = inject(ComplianceService);

  applications: any[] = [];
  selectedMatch: any = null;
  selectedCompliance: any = null;
  selectedApp: any = null;
  
  overrideReason = '';
  bookingError = '';
  bookingSuccess = false;

  ngOnInit() {
    this.loadApplications();
  }

  loadApplications() {
    this.shiftService.getApplications({ status: 'APPLIED' }).subscribe({
      next: (res) => this.applications = res.results
    });
  }

  viewMatchDetails(app: any) {
    this.selectedCompliance = null;
    this.matchingService.getShiftMatches(app.shift).subscribe({
      next: (res) => {
        const match = res.data.find((m: any) => m.professional_id === app.professional);
        if (match) {
          this.selectedMatch = {
            score: match.match_score,
            details: match.details
          };
        }
      }
    });
  }

  checkCompliance(app: any) {
    this.selectedMatch = null;
    this.selectedApp = app;
    this.overrideReason = '';
    this.bookingError = '';
    this.bookingSuccess = false;

    this.complianceService.checkCompliance(app.professional, app.shift).subscribe({
      next: (res) => {
        this.selectedCompliance = res.data;
      }
    });
  }

  sendOffer(app: any) {
    this.shiftService.sendOffer(app.shift, app.professional).subscribe({
      next: () => this.loadApplications()
    });
  }

  confirmBooking() {
    if (!this.selectedApp) return;
    this.bookingError = '';
    this.bookingSuccess = false;

    this.shiftService.confirmBooking(this.selectedApp.shift, this.selectedApp.professional, this.overrideReason).subscribe({
      next: () => {
        this.bookingSuccess = true;
        this.selectedCompliance = null;
        this.loadApplications();
      },
      error: (err) => {
        this.bookingError = err.error?.message || 'Placement confirmation failed. Check scheduling conflicts or missing credentials.';
      }
    });
  }
}
