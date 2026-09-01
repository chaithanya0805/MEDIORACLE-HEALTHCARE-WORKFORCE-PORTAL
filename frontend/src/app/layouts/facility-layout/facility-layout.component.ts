import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterOutlet, RouterLinkActive } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-facility-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive],
  template: `
    <div class="min-h-screen flex bg-slate-50">
      <!-- Sidebar -->
      <aside class="w-64 bg-slate-900 text-white flex flex-col justify-between p-4 shadow-xl">
        <div>
          <!-- Logo -->
          <div class="flex items-center gap-3 px-2 py-4 mb-6">
            <div class="w-8 h-8 rounded-lg bg-sky-500 flex items-center justify-center font-bold text-lg text-white">N</div>
            <span class="font-bold text-lg tracking-wider text-slate-100 font-sans">MediOracle</span>
          </div>

          <!-- Navigation Links -->
          <nav class="space-y-1">
            <a routerLink="dashboard" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z" /></svg>
              <span>Dashboard</span>
            </a>
            <a routerLink="shifts" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              <span>Manage Shifts</span>
            </a>
            <a routerLink="applications" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              <span>Applications</span>
            </a>
            <a routerLink="timesheets" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
              <span>Timesheets</span>
            </a>
            <a routerLink="analytics" routerLinkActive="bg-slate-800 text-white" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/50 transition duration-150">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
              <span>Staffing Analytics</span>
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
          <h1 class="text-xl font-bold text-slate-800 tracking-tight font-sans">Nexgile – MediOracle Portal</h1>
          <div class="flex items-center gap-4">
            <div class="text-sm text-slate-500">Demo Session</div>
            <div class="h-8 w-px bg-slate-200"></div>
            <span class="px-2.5 py-1 rounded-full text-xs font-semibold bg-sky-100 text-sky-800">{{ user?.role }}</span>
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
export class FacilityLayoutComponent {
  authService = inject(AuthService);
  router = inject(Router);

  get user() {
    return this.authService.currentUser;
  }

  logout() {
    this.authService.logout().subscribe();
  }
}
