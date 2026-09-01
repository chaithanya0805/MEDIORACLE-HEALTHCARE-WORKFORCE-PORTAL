import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-slate-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <!-- Background gradients -->
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.15),transparent_45%)]"></div>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_bottom_left,rgba(20,184,166,0.15),transparent_45%)]"></div>
      
      <!-- Card -->
      <div class="max-w-md w-full space-y-8 bg-slate-950/70 border border-slate-800 backdrop-blur-xl p-8 rounded-2xl shadow-2xl relative z-10">
        <div>
          <div class="mx-auto h-12 w-12 rounded-xl bg-sky-500 flex items-center justify-center font-bold text-2xl text-white">N</div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-white tracking-tight font-sans">MediOracle Portal</h2>
          <p class="mt-2 text-center text-sm text-slate-400">
            Sign in to manage healthcare staffing and shifts.
          </p>
        </div>

        <form class="mt-8 space-y-6" [formGroup]="loginForm" (ngSubmit)="onSubmit()">
          <!-- Error Alert -->
          <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm">
            {{ errorMessage }}
          </div>

          <div class="space-y-4">
            <div>
              <label for="email" class="block text-sm font-semibold text-slate-300 font-sans">Email address</label>
              <input id="email" type="email" formControlName="email" required
                class="mt-1 block w-full px-3 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent text-sm">
            </div>

            <div>
              <label for="password" class="block text-sm font-semibold text-slate-300 font-sans">Password</label>
              <input id="password" type="password" formControlName="password" required
                class="mt-1 block w-full px-3 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent text-sm">
            </div>
          </div>

          <div class="flex items-center justify-between text-sm">
            <a routerLink="/forgot-password" class="font-medium text-sky-400 hover:text-sky-300 font-sans">Forgot your password?</a>
          </div>

          <button type="submit" [disabled]="loginForm.invalid || loading"
            class="w-full py-2.5 px-4 bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white font-bold rounded-xl text-sm transition duration-150 shadow-lg shadow-sky-500/20 font-sans">
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 mt-4 font-sans">
          Don't have an account?
          <a routerLink="/register" class="font-medium text-sky-400 hover:text-sky-300">Register now</a>
        </p>

        <!-- Quick Demo Accounts -->
        <div class="border-t border-slate-800/80 pt-4 mt-6">
          <span class="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-2 font-sans">Quick Demo Access</span>
          <div class="grid grid-cols-2 gap-2 text-xs">
            <button (click)="fillCreds('facility@nexgile.com')" class="text-left bg-slate-900 hover:bg-slate-800 p-2 rounded border border-slate-800/60 text-slate-400 hover:text-white transition font-sans">
              <span class="font-bold block text-slate-200">Facility Admin</span>
              facility&#64;nexgile.com
            </button>
            <button (click)="fillCreds('professional1@nexgile.com')" class="text-left bg-slate-900 hover:bg-slate-800 p-2 rounded border border-slate-800/60 text-slate-400 hover:text-white transition font-sans">
              <span class="font-bold block text-slate-200">Professional (RN)</span>
              professional1&#64;nexgile.com
            </button>
          </div>
        </div>
      </div>
    </div>
  `
})
export class LoginComponent {
  fb = inject(FormBuilder);
  authService = inject(AuthService);
  router = inject(Router);

  loginForm = this.fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  });

  loading = false;
  errorMessage = '';

  fillCreds(email: string) {
    this.loginForm.patchValue({
      email: email,
      password: 'password123'
    });
  }

  onSubmit() {
    if (this.loginForm.invalid) return;
    this.loading = true;
    this.errorMessage = '';
    
    this.authService.login(this.loginForm.value).subscribe({
      next: (res) => {
        const role = res.user.role;
        if (role === 'PROFESSIONAL') {
          this.router.navigate(['/professional/dashboard']);
        } else {
          this.router.navigate(['/facility/dashboard']);
        }
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.non_field_errors?.[0] || err.error?.detail || 'Invalid email or password. Please try again.';
      }
    });
  }
}
