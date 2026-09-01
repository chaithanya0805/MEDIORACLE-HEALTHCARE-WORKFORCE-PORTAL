import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TimekeepingService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api/timekeeping/timesheets';

  getTimesheets(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/`, { params });
  }

  getTimesheet(id: number) {
    return this.http.get<any>(`${this.baseUrl}/${id}/`);
  }

  clockIn(id: number, latitude?: number, longitude?: number) {
    return this.http.post<any>(`${this.baseUrl}/${id}/clock_in/`, { latitude, longitude });
  }

  breakStart(id: number, latitude?: number, longitude?: number) {
    return this.http.post<any>(`${this.baseUrl}/${id}/break_start/`, { latitude, longitude });
  }

  breakEnd(id: number, latitude?: number, longitude?: number) {
    return this.http.post<any>(`${this.baseUrl}/${id}/break_end/`, { latitude, longitude });
  }

  clockOut(id: number, latitude?: number, longitude?: number) {
    return this.http.post<any>(`${this.baseUrl}/${id}/clock_out/`, { latitude, longitude });
  }

  submitTimesheet(id: number, signature: string) {
    return this.http.post<any>(`${this.baseUrl}/${id}/submit/`, { signature });
  }

  approveTimesheet(id: number) {
    return this.http.post<any>(`${this.baseUrl}/${id}/approve/`, {});
  }

  correctTimesheet(id: number, hours: number, reason: string) {
    return this.http.post<any>(`${this.baseUrl}/${id}/correct/`, { total_hours: hours, reason });
  }
}
