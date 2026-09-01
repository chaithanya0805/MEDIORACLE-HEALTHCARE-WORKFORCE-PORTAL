import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { roleGuard } from './core/guards/role.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent)
  },
  {
    path: 'register',
    loadComponent: () => import('./features/auth/register/register.component').then(m => m.RegisterComponent)
  },
  {
    path: 'forgot-password',
    loadComponent: () => import('./features/auth/forgot-password/forgot-password.component').then(m => m.ForgotPasswordComponent)
  },
  {
    path: 'reset-password',
    loadComponent: () => import('./features/auth/reset-password/reset-password.component').then(m => m.ResetPasswordComponent)
  },
  {
    path: 'facility',
    canActivate: [authGuard, roleGuard],
    data: { allowedRoles: ['FACILITY_ADMIN', 'HR_WORKFORCE_MANAGER', 'SUPER_ADMIN'] },
    loadComponent: () => import('./layouts/facility-layout/facility-layout.component').then(m => m.FacilityLayoutComponent),
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/facility/dashboard/dashboard.component').then(m => m.FacilityDashboardComponent)
      },
      {
        path: 'shifts',
        loadComponent: () => import('./features/facility/shifts/shifts.component').then(m => m.FacilityShiftsComponent)
      },
      {
        path: 'applications',
        loadComponent: () => import('./features/facility/applications/applications.component').then(m => m.FacilityApplicationsComponent)
      },
      {
        path: 'timesheets',
        loadComponent: () => import('./features/facility/timesheets/timesheets.component').then(m => m.FacilityTimesheetsComponent)
      },
      {
        path: 'analytics',
        loadComponent: () => import('./features/facility/analytics/analytics.component').then(m => m.FacilityAnalyticsComponent)
      }
    ]
  },
  {
    path: 'professional',
    canActivate: [authGuard, roleGuard],
    data: { allowedRoles: ['PROFESSIONAL', 'SUPER_ADMIN'] },
    loadComponent: () => import('./layouts/professional-layout/professional-layout.component').then(m => m.ProfessionalLayoutComponent),
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./features/professional/dashboard/dashboard.component').then(m => m.ProfessionalDashboardComponent)
      },
      {
        path: 'profile',
        loadComponent: () => import('./features/professional/profile/profile.component').then(m => m.ProfessionalProfileComponent)
      },
      {
        path: 'shifts',
        loadComponent: () => import('./features/professional/shifts/shifts.component').then(m => m.ProfessionalShiftsComponent)
      },
      {
        path: 'credentials',
        loadComponent: () => import('./features/professional/credentials/credentials.component').then(m => m.ProfessionalCredentialsComponent)
      },
      {
        path: 'timesheets',
        loadComponent: () => import('./features/professional/timesheets/timesheets.component').then(m => m.ProfessionalTimesheetsComponent)
      }
    ]
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
