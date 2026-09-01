import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ProfessionalService } from '../../../core/services/professional.service';

@Component({
  selector: 'app-professional-profile',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Professional Profile Settings</h2>

      <div *ngIf="profile" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Main Bio Card -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 text-center space-y-4">
          <div class="w-24 h-24 rounded-full bg-slate-100 flex items-center justify-center font-bold text-3xl text-slate-400 mx-auto">
            {{ profile.user_details?.first_name ? profile.user_details.first_name[0] : 'U' }}
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-800">{{ profile.user_details?.first_name }} {{ profile.user_details?.last_name }}</h3>
            <span class="text-xs text-slate-400 font-semibold">{{ profile.role_name }} • {{ profile.specialty_name }}</span>
          </div>
          
          <div class="bg-slate-50 p-3 rounded-xl text-xs flex justify-around">
            <div>
              <span class="text-slate-400 block mb-0.5">Rating</span>
              <span class="font-extrabold text-slate-700">{{ profile.rating }}/5.0</span>
            </div>
            <div class="h-8 w-px bg-slate-200"></div>
            <div>
              <span class="text-slate-400 block mb-0.5">Reliability</span>
              <span class="font-extrabold text-slate-700">{{ profile.reliability_score }}%</span>
            </div>
          </div>
        </div>

        <!-- Settings fields -->
        <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 lg:col-span-2 space-y-4">
          <div class="border-b border-slate-100 pb-3">
            <h3 class="font-bold text-slate-800">Account Particulars</h3>
          </div>

          <form [formGroup]="profileForm" (ngSubmit)="onSubmit()" class="space-y-4 text-xs">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-500 mb-1">Preferred Hourly Rate (€)</label>
                <input type="number" formControlName="preferred_rate" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
              </div>
              <div>
                <label class="block font-semibold text-slate-500 mb-1">Minimum Rate (€)</label>
                <input type="number" formControlName="minimum_rate" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block font-semibold text-slate-500 mb-1">Max Commute (km)</label>
                <input type="number" formControlName="preferred_commute_distance" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
              </div>
              <div>
                <label class="block font-semibold text-slate-500 mb-1">Availability Status</label>
                <select formControlName="availability_status" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
                  <option value="AVAILABLE">Available</option>
                  <option value="ON_LEAVE">On Leave</option>
                  <option value="SUSPENDED">Suspended</option>
                </select>
              </div>
            </div>

            <div>
              <label class="block font-semibold text-slate-500 mb-1">Biography / Summary</label>
              <textarea formControlName="bio" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl h-24 focus:outline-none"></textarea>
            </div>

            <div class="flex justify-end pt-2">
              <button type="submit" [disabled]="profileForm.invalid || loading" class="px-4 py-2 bg-sky-500 text-white font-bold rounded-xl hover:bg-sky-600 transition">
                {{ loading ? 'Saving...' : 'Save Settings' }}
              </button>
            </div>
            <div *ngIf="successMessage" class="text-teal-600 font-semibold mt-2">✓ Settings saved successfully!</div>
          </form>
        </div>
      </div>
    </div>
  `
})
export class ProfessionalProfileComponent implements OnInit {
  fb = inject(FormBuilder);
  profService = inject(ProfessionalService);

  profile: any = null;
  profileForm = this.fb.group({
    preferred_rate: ['', Validators.required],
    minimum_rate: ['', Validators.required],
    preferred_commute_distance: ['', Validators.required],
    availability_status: ['', Validators.required],
    bio: ['']
  });

  loading = false;
  successMessage = false;

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.profService.getProfiles().subscribe({
      next: (res) => {
        if (res.results && res.results.length > 0) {
          this.profile = res.results[0];
          this.profileForm.patchValue({
            preferred_rate: this.profile.preferred_rate,
            minimum_rate: this.profile.minimum_rate,
            preferred_commute_distance: this.profile.preferred_commute_distance,
            availability_status: this.profile.availability_status,
            bio: this.profile.bio
          });
        }
      }
    });
  }

  onSubmit() {
    if (this.profileForm.invalid || !this.profile) return;
    this.loading = true;
    this.successMessage = false;

    this.profService.updateProfile(this.profile.id, {
      ...this.profile,
      ...this.profileForm.value
    }).subscribe({
      next: () => {
        this.loading = false;
        this.successMessage = true;
        this.loadProfile();
      }
    });
  }
}
