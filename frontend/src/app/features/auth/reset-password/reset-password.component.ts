import { Component, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-slate-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.15),transparent_45%)]"></div>
      
      <div class="max-w-md w-full space-y-8 bg-slate-950/70 border border-slate-800 backdrop-blur-xl p-8 rounded-2xl shadow-2xl relative z-10">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-white tracking-tight">Reset Password</h2>
          <p class="mt-2 text-center text-sm text-slate-400">Choose a strong, secure new password for your account</p>
        </div>

        <form (submit)="onSubmit()" class="mt-8 space-y-6">
          <div *ngIf="successMessage" class="bg-teal-500/10 border border-teal-500/20 text-teal-400 p-4 rounded-xl text-sm font-semibold text-center">
            {{ successMessage }}
          </div>
          <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm font-semibold text-center">
            {{ errorMessage }}
          </div>

          <div class="rounded-md shadow-sm space-y-4">
            <div>
              <label for="new-password" class="sr-only">New Password</label>
              <input id="new-password" name="newPassword" type="password" required [(ngModel)]="newPassword"
                class="appearance-none rounded-xl relative block w-full px-4 py-3 bg-slate-900 border border-slate-800 placeholder-slate-500 text-white focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 focus:z-10 text-sm"
                placeholder="New Password">
            </div>
            <div>
              <label for="confirm-password" class="sr-only">Confirm New Password</label>
              <input id="confirm-password" name="confirmPassword" type="password" required [(ngModel)]="confirmPassword"
                class="appearance-none rounded-xl relative block w-full px-4 py-3 bg-slate-900 border border-slate-800 placeholder-slate-500 text-white focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 focus:z-10 text-sm"
                placeholder="Confirm New Password">
            </div>
          </div>

          <div>
            <button type="submit" [disabled]="loading || !newPassword || !confirmPassword"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-sky-500 hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition disabled:opacity-50">
              <span *ngIf="loading">Resetting...</span>
              <span *ngIf="!loading">Reset Password</span>
            </button>
          </div>
        </form>

        <div class="text-center mt-4">
          <a routerLink="/login" class="font-medium text-sky-400 hover:text-sky-300 text-sm transition">Back to Login</a>
        </div>
      </div>
    </div>
  `
})
export class ResetPasswordComponent implements OnInit {
  route = inject(ActivatedRoute);
  router = inject(Router);
  authService = inject(AuthService);

  email = '';
  token = '';
  newPassword = '';
  confirmPassword = '';
  loading = false;
  successMessage = '';
  errorMessage = '';

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      this.email = params['email'] || '';
      this.token = params['token'] || '';
    });

    if (!this.email || !this.token) {
      this.errorMessage = 'Invalid password reset link. Please check your email or request a new reset link.';
    }
  }

  onSubmit() {
    if (!this.email || !this.token) return;
    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      return;
    }

    this.loading = true;
    this.successMessage = '';
    this.errorMessage = '';

    const payload = {
      email: this.email,
      token: this.token,
      new_password: this.newPassword
    };

    this.authService.resetPassword(payload).subscribe({
      next: (res) => {
        this.loading = false;
        this.successMessage = res.message || 'Password reset successfully!';
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.message || 'Failed to reset password. The link may have expired.';
      }
    });
  }
}
