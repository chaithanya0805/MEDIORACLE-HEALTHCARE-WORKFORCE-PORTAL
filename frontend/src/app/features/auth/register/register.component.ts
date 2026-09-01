import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../core/services/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  template: `
    <div class="min-h-screen flex items-center justify-center bg-slate-900 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden font-sans">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.15),transparent_45%)]"></div>
      
      <div class="max-w-md w-full space-y-8 bg-slate-950/70 border border-slate-800 backdrop-blur-xl p-8 rounded-2xl shadow-2xl relative z-10">
        <div>
          <h2 class="text-center text-3xl font-extrabold text-white tracking-tight">Create your Account</h2>
          <p class="mt-2 text-center text-sm text-slate-400">Join MediOracle Healthcare Workforce Portal</p>
        </div>

        <form class="mt-6 space-y-4" [formGroup]="registerForm" (ngSubmit)="onSubmit()">
          <div *ngIf="errorMessage" class="bg-rose-500/10 border border-rose-500/20 text-rose-400 p-4 rounded-xl text-sm">
            {{ errorMessage }}
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-semibold text-slate-300">First Name</label>
              <input type="text" formControlName="first_name" required
                class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-300">Last Name</label>
              <input type="text" formControlName="last_name" required
                class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-300">Email address</label>
            <input type="email" formControlName="email" required
              class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-300">Phone</label>
            <input type="text" formControlName="phone" required
              class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-300">Role</label>
            <select formControlName="role" required
              class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
              <option value="PROFESSIONAL">Healthcare Professional</option>
              <option value="FACILITY_ADMIN">Facility Admin</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-slate-300">Password</label>
            <input type="password" formControlName="password" required
              class="mt-1 block w-full px-3 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-sky-500 text-sm">
          </div>

          <button type="submit" [disabled]="registerForm.invalid || loading"
            class="w-full py-2.5 px-4 bg-sky-500 hover:bg-sky-600 disabled:opacity-50 text-white font-bold rounded-xl text-sm transition duration-150 shadow-lg shadow-sky-500/20">
            {{ loading ? 'Creating Account...' : 'Register' }}
          </button>
        </form>

        <p class="text-center text-sm text-slate-500 mt-4">
          Already have an account?
          <a routerLink="/login" class="font-medium text-sky-400 hover:text-sky-300">Sign in</a>
        </p>
      </div>
    </div>
  `
})
export class RegisterComponent {
  fb = inject(FormBuilder);
  authService = inject(AuthService);
  router = inject(Router);

  registerForm = this.fb.group({
    first_name: ['', Validators.required],
    last_name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
    phone: ['', Validators.required],
    role: ['PROFESSIONAL', Validators.required],
    password: ['', [Validators.required, Validators.minLength(6)]]
  });

  loading = false;
  errorMessage = '';

  onSubmit() {
    if (this.registerForm.invalid) return;
    this.loading = true;
    this.errorMessage = '';
    
    this.authService.register(this.registerForm.value).subscribe({
      next: (res) => {
        if (res.user.role === 'PROFESSIONAL') {
          this.router.navigate(['/professional/dashboard']);
        } else {
          this.router.navigate(['/facility/dashboard']);
        }
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.message || 'Registration failed. Please check inputs.';
      }
    });
  }
}
