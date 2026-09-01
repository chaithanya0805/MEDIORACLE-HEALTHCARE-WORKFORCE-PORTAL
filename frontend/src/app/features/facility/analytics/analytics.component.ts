import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsService } from '../../../core/services/analytics.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-facility-analytics',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Staffing Analytics & Demand Forecasting</h2>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- What-If Forecasting Slider -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 lg:col-span-1 space-y-6">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-slate-800">What-If Census Simulator</h3>
            <span class="text-xs text-slate-400">Simulate hospital census surge and calculate demand</span>
          </div>

          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-sm font-semibold text-slate-700">Projected Census Increase</span>
              <span class="text-lg font-extrabold text-sky-600">+{{ censusSurge }}%</span>
            </div>
            
            <input type="range" min="0" max="50" step="5" [(ngModel)]="censusSurge" (change)="onSurgeChange()"
              class="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer accent-sky-500">
            
            <div class="flex justify-between text-2xs font-semibold text-slate-400 px-1">
              <span>0% (Base)</span>
              <span>25%</span>
              <span>50% (Max)</span>
            </div>
          </div>

          <!-- Simulation results -->
          <div *ngIf="forecastData" class="space-y-4 pt-4 border-t border-slate-100 text-xs">
            <div class="flex justify-between py-1.5 border-b border-slate-50">
              <span class="text-slate-500 font-medium">Base Staff Capacity</span>
              <span class="font-bold text-slate-800">{{ forecastData.current_staff_count }} workers</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-50">
              <span class="text-slate-500 font-medium">Additional Staff Needed</span>
              <span class="font-bold text-amber-600">+{{ forecastData.additional_staff_needed }} workers</span>
            </div>
            <div class="flex justify-between py-1.5 border-b border-slate-50">
              <span class="text-slate-500 font-medium">Projected Shift Cost</span>
              <span class="font-bold text-slate-800">€{{ forecastData.estimated_shift_cost | number:'1.2-2' }}</span>
            </div>
            <div class="flex justify-between py-1.5">
              <span class="text-slate-500 font-medium">Expected Staff Shortage</span>
              <span class="font-bold text-rose-600">{{ forecastData.expected_shortage }} workers</span>
            </div>
          </div>
        </div>

        <!-- Recommendations Panel -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 lg:col-span-2 space-y-6">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-slate-800">Recommended Placement Staffing</h3>
            <span class="text-xs text-slate-400">AI-suggested shift listings based on forecast</span>
          </div>

          <div class="space-y-4">
            <div *ngFor="let rec of forecastData?.recommended_shifts" class="flex gap-4 p-4 bg-slate-50 rounded-2xl border border-slate-100 hover:shadow-sm transition">
              <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-600 flex items-center justify-center font-bold text-sm shrink-0">
                AI
              </div>
              <div class="space-y-1">
                <div class="font-bold text-slate-800 text-sm">{{ rec.role }} Needed</div>
                <div class="text-xs text-slate-500 font-medium">Schedule: {{ rec.timing }}</div>
                <p class="text-xs text-slate-400 leading-relaxed">{{ rec.reason }}</p>
              </div>
            </div>
            <div *ngIf="!forecastData?.recommended_shifts?.length" class="text-center py-8 text-slate-400">
              Increase the census slider to generate automated staffing recommendations.
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class FacilityAnalyticsComponent implements OnInit {
  analyticsService = inject(AnalyticsService);

  censusSurge = 15;
  forecastData: any = null;

  ngOnInit() {
    this.onSurgeChange();
  }

  onSurgeChange() {
    this.analyticsService.simulateWhatIf(this.censusSurge).subscribe({
      next: (res) => this.forecastData = res.data
    });
  }
}
