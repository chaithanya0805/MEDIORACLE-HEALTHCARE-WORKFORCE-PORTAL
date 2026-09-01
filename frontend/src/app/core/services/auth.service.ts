import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { BehaviorSubject, tap } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private http = inject(HttpClient);
  private router = inject(Router);
  private baseUrl = `${environment.apiUrl}/auth`;
  private userSubject = new BehaviorSubject<any>(JSON.parse(localStorage.getItem('user') || 'null'));
  user$ = this.userSubject.asObservable();

  login(credentials: any) {
    return this.http.post<any>(`${this.baseUrl}/login/`, credentials).pipe(
      tap(res => {
        if (res.access) {
          localStorage.setItem('access_token', res.access);
          localStorage.setItem('refresh_token', res.refresh);
          localStorage.setItem('user', JSON.stringify(res.user));
          this.userSubject.next(res.user);
        }
      })
    );
  }

  register(data: any) {
    return this.http.post<any>(`${this.baseUrl}/register/`, data).pipe(
      tap(res => {
        if (res.access) {
          localStorage.setItem('access_token', res.access);
          localStorage.setItem('refresh_token', res.refresh);
          localStorage.setItem('user', JSON.stringify(res.user));
          this.userSubject.next(res.user);
        }
      })
    );
  }

  logout() {
    const refresh = localStorage.getItem('refresh_token');
    return this.http.post<any>(`${this.baseUrl}/logout/`, { refresh }).pipe(
      tap({
        finalize: () => {
          localStorage.clear();
          this.userSubject.next(null);
          this.router.navigate(['/login']);
        }
      })
    );
  }

  get currentUser() {
    return this.userSubject.value;
  }

  forgotPassword(email: string) {
    return this.http.post<any>(`${this.baseUrl}/forgot-password/`, { email });
  }

  resetPassword(data: any) {
    return this.http.post<any>(`${this.baseUrl}/reset-password/`, data);
  }
}
