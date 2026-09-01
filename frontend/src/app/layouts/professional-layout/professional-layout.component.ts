import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterOutlet, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-professional-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="min-h-screen flex bg-slate-50">
      <!-- Sidebar -->
      <aside class="w-64 bg-slate-900 text-white flex flex-col justify-between p-4 shadow-xl">
        <div>
          <!-- Logo -->
          <div class="flex items-center gap-3 px-2 py-4 mb-6">
            <div class="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center font-bold text-lg text-white">N</div>
            <span class="font-bold text-lg tracking-wider text-slate-100 font-sans">MediOracle</span>
          </div>

          <!-- Navigation Links -->
          <nav class="space-y-1">
            <a routerLink="dashboard" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
              <span>Dashboard</span>
            </a>
            <a routerLink="profile" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
              <span>My Profile</span>
            </a>
            <a routerLink="shifts" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              <span>Find Shifts</span>
            </a>
            <a routerLink="credentials" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
              <span>My Credentials</span>
            </a>
            <a routerLink="timesheets" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
              <span>My Timesheets</span>
            </a>
          </nav>
        </div>

        <!-- Sidebar footer -->
        <div class="border-t border-slate-800 pt-4">
          <div class="flex items-center gap-3 px-2 mb-4">
            <div class="w-10 h-10 rounded-full bg-slate-700 flex items-center justify-center font-bold text-white uppercase">{{ user?.name ? user.name[0] : 'U' }}</div>
            <div class="overflow-hidden">
              <div class="font-semibold text-sm truncate text-slate-200">{{ user?.name }}</div>
              <div class="text-xs text-slate-500 truncate">{{ user?.role }}</div>
            </div>
          </div>
          <button (click)="logout()" class="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-rose-400 hover:text-white hover:bg-rose-600 transition duration-150">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
            <span>Log out</span>
          </button>
        </div>
      </aside>

      <!-- Main Content Area -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Header -->
        <header class="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-8 shadow-sm">
          <h1 class="text-xl font-bold text-slate-800 tracking-tight font-sans">Welcome, {{ user?.name }}</h1>
          <div class="flex items-center gap-4">
            <div class="text-sm text-slate-500">Professional Portal</div>
            <div class="h-8 w-px bg-slate-200"></div>
            <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-teal-100 text-teal-800">{{ user?.role }}</span>
          </div>
        </header>

        <!-- Dynamic Page Router Outlet -->
        <main class="flex-1 overflow-y-auto p-8">
          <router-outlet></router-outlet>
        </main>
      </div>
    </div>
  `
})
export class ProfessionalLayoutComponent {
  authService = inject(AuthService);
  router = inject(Router);

  get user() {
    return this.authService.currentUser;
  }

  logout() {
    this.authService.logout().subscribe();
  }
}
