import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ProfessionalService } from '../../../core/services/professional.service';

@Component({
  selector: 'app-professional-credentials',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <div class="space-y-6 font-sans">
      <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-slate-800 tracking-tight font-sans">Compliance Credentials</h2>
        <button (click)="showUpload = !showUpload" class="px-4 py-2 bg-sky-500 hover:bg-sky-600 text-white font-bold rounded-xl text-sm transition shadow-lg shadow-sky-500/20 font-sans">
          {{ showUpload ? 'Cancel' : '+ Upload Credential' }}
        </button>
      </div>

      <!-- Upload Form -->
      <div *ngIf="showUpload" class="bg-white border border-slate-200/80 rounded-2xl shadow-sm p-6 space-y-4">
        <div class="border-b border-slate-100 pb-3">
          <h3 class="font-bold text-slate-800">Upload compliance documentation</h3>
        </div>

        <form [formGroup]="credForm" (ngSubmit)="onSubmit()" class="space-y-4 text-xs">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Credential Type</label>
              <select formControlName="credential_type" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
                <option *ngFor="let ct of types" [value]="ct.id">{{ ct.name }} ({{ ct.code }})</option>
              </select>
            </div>
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Registration / Cert Number</label>
              <input type="text" formControlName="credential_number" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
            </div>
          </div>

          <div class="grid grid-cols-3 gap-4">
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Issuing Authority</label>
              <input type="text" formControlName="issuing_authority" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
            </div>
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Issue Date</label>
              <input type="date" formControlName="issue_date" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
            </div>
            <div>
              <label class="block font-semibold text-slate-500 mb-1">Expiry Date</label>
              <input type="date" formControlName="expiry_date" class="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
            </div>
          </div>

          <div>
            <label class="block font-semibold text-slate-500 mb-1">Upload Document File (PDF/Image)</label>
            <input type="file" (change)="onFileChange($event)" class="w-full p-2 bg-slate-50 border border-slate-200 rounded-xl focus:outline-none">
          </div>

          <div class="flex justify-end pt-2">
            <button type="submit" [disabled]="credForm.invalid || loading" class="px-4 py-2 bg-sky-500 text-white font-bold rounded-xl hover:bg-sky-600 transition shadow font-sans">
              Submit for Verification
            </button>
          </div>
        </form>
      </div>

      <!-- Credential list -->
      <div class="bg-white border border-slate-200/80 rounded-2xl shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <span class="font-bold text-slate-800">My Uploaded Credentials</span>
        </div>
        <table class="w-full text-left border-collapse text-sm">
          <thead>
            <tr class="border-b border-slate-100 text-xs font-semibold uppercase text-slate-400 bg-slate-50/20">
              <th class="px-6 py-3">Credential Name</th>
              <th class="px-6 py-3">Number / Authority</th>
              <th class="px-6 py-3">Expiry Date</th>
              <th class="px-6 py-3">Verification</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 text-slate-700">
            <tr *ngFor="let c of credentials" class="hover:bg-slate-50/30 transition">
              <td class="px-6 py-4">
                <div class="font-bold text-slate-800">{{ c.credential_type_name }}</div>
              </td>
              <td class="px-6 py-4">
                <div>No: {{ c.credential_number }}</div>
                <div class="text-xs text-slate-400">{{ c.issuing_authority }}</div>
              </td>
              <td class="px-6 py-4">
                <div [ngClass]="isExpiringSoon(c.expiry_date) ? 'text-rose-500 font-semibold' : ''">{{ c.expiry_date }}</div>
                <div class="text-xs text-slate-400">{{ getRemainingDays(c.expiry_date) }} days left</div>
              </td>
              <td class="px-6 py-4">
                <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold"
                  [ngClass]="{
                    'bg-teal-100 text-teal-800': c.verification_status === 'VERIFIED',
                    'bg-amber-100 text-amber-800': c.verification_status === 'PENDING',
                    'bg-rose-100 text-rose-800': c.verification_status === 'REJECTED'
                  }">
                  {{ c.verification_status }}
                </span>
              </td>
            </tr>
            <tr *ngIf="credentials.length === 0">
              <td colspan="4" class="px-6 py-8 text-center text-slate-400">No credentials uploaded yet. Please click Upload to verify compliance.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `
})
export class ProfessionalCredentialsComponent implements OnInit {
  fb = inject(FormBuilder);
  profService = inject(ProfessionalService);

  credentials: any[] = [];
  types: any[] = [];
  showUpload = false;
  loading = false;
  selectedFile: File | null = null;

  credForm = this.fb.group({
    credential_type: ['', Validators.required],
    credential_number: ['', Validators.required],
    issuing_authority: ['', Validators.required],
    issue_date: ['', Validators.required],
    expiry_date: ['', Validators.required]
  });

  ngOnInit() {
    this.loadCredentials();
    this.loadTypes();
  }

  loadCredentials() {
    this.profService.getCredentials().subscribe({
      next: (res) => this.credentials = res.results
    });
  }

  loadTypes() {
    this.profService.getCredentialTypes().subscribe({
      next: (res) => {
        this.types = res.results;
        if (this.types.length > 0) {
          this.credForm.patchValue({ credential_type: this.types[0].id });
        }
      }
    });
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
    }
  }

  onSubmit() {
    if (this.credForm.invalid) return;
    this.loading = true;

    const fd = new FormData();
    fd.append('credential_type', this.credForm.get('credential_type')?.value || '');
    fd.append('credential_number', this.credForm.get('credential_number')?.value || '');
    fd.append('issuing_authority', this.credForm.get('issuing_authority')?.value || '');
    fd.append('issue_date', this.credForm.get('issue_date')?.value || '');
    fd.append('expiry_date', this.credForm.get('expiry_date')?.value || '');
    if (this.selectedFile) {
      fd.append('document_file', this.selectedFile);
    }

    this.profService.uploadCredential(fd).subscribe({
      next: () => {
        this.loading = false;
        this.showUpload = false;
        this.credForm.reset();
        this.selectedFile = null;
        this.loadCredentials();
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  isExpiringSoon(expDate: string): boolean {
    const diff = new Date(expDate).getTime() - new Date().getTime();
    return diff < 1000 * 60 * 60 * 24 * 30; // 30 days
  }

  getRemainingDays(expDate: string): number {
    const diff = new Date(expDate).getTime() - new Date().getTime();
    return Math.max(Math.ceil(diff / (1000 * 60 * 60 * 24)), 0);
  }
}
