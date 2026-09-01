import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const roleGuard: CanActivateFn = (route, state) => {
  const router = inject(Router);
  const userStr = localStorage.getItem('user');
  const allowedRoles = route.data['allowedRoles'] as string[];

  if (userStr) {
    const user = JSON.parse(userStr);
    if (user && (user.role === 'SUPER_ADMIN' || allowedRoles.includes(user.role))) {
      return true;
    }
  }

  router.navigate(['/login']);
  return false;
};
