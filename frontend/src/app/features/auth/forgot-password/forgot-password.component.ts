import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-slate-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.15),transparent_45%)]"></div>
      
      <div class="max-w-md w-full space-y-8 bg-slate-950/70 border border-slate-800 backdrop-blur-xl p-8 rounded-2xl shadow-2xl relative z-10">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-white tracking-tight">Forgot Password</h2>
          <p class="mt-2 text-center text-sm text-slate-400">Enter your email address to receive a secure recovery link</p>
        </div>

        <form (submit)="onSubmit()" class="mt-8 space-y-6">
          <div *ngIf="successMessage" class="bg-teal-500/10 border border-teal-500/20 text-teal-400 p-4 rounded-xl text-sm font-semibold text-center">
            {{ successMessage }}
          </div>
          <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm font-semibold text-center">
            {{ errorMessage }}
          </div>

          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="email-address" class="sr-only">Email address</label>
              <input id="email-address" name="email" type="email" required [(ngModel)]="email"
                class="appearance-none rounded-xl relative block w-full px-4 py-3 bg-slate-900 border border-slate-800 placeholder-slate-500 text-white focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 focus:z-10 text-sm"
                placeholder="Email address">
            </div>
          </div>

          <div>
            <button type="submit" [disabled]="loading"
              class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-sky-500 hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-sky-500 transition disabled:opacity-50">
              <span *ngIf="loading">Sending...</span>
              <span *ngIf="!loading">Send Reset Link</span>
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
export class ForgotPasswordComponent {
  authService = inject(AuthService);

  email = '';
  loading = false;
  successMessage = '';
  errorMessage = '';

  onSubmit() {
    if (!this.email) return;
    this.loading = true;
    this.successMessage = '';
    this.errorMessage = '';

    this.authService.forgotPassword(this.email).subscribe({
      next: (res) => {
        this.loading = false;
        this.successMessage = res.message || 'If this email is registered, a password reset link has been sent.';
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.message || 'Failed to request password reset. Please try again.';
      }
    });
  }
}
