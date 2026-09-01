import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ShiftService {
  private http = inject(HttpClient);
  private baseUrl = 'https://medioracle-backend.onrender.com/api/shifts';

  getShifts(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/shifts/`, { params });
  }

  getShift(id: number) {
    return this.http.get<any>(`${this.baseUrl}/shifts/${id}/`);
  }

  createShift(data: any) {
    return this.http.post<any>(`${this.baseUrl}/shifts/`, data);
  }

  publishShift(id: number) {
    return this.http.post<any>(`${this.baseUrl}/shifts/${id}/publish/`, {});
  }

  applyToShift(id: number) {
    return this.http.post<any>(`${this.baseUrl}/shifts/${id}/apply/`, {});
  }

  sendOffer(id: number, professionalId: number) {
    return this.http.post<any>(`${this.baseUrl}/shifts/${id}/offer/`, { professional_id: professionalId });
  }

  confirmBooking(id: number, professionalId: number, overrideReason?: string) {
    return this.http.post<any>(`${this.baseUrl}/shifts/${id}/confirm_booking/`, {
      professional_id: professionalId,
      override_reason: overrideReason
    });
  }

  getApplications(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/applications/`, { params });
  }

  getOffers(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/offers/`, { params });
  }

  acceptOffer(id: number) {
    return this.http.post<any>(`${this.baseUrl}/offers/${id}/accept/`, {});
  }

  rejectOffer(id: number) {
    return this.http.post<any>(`${this.baseUrl}/offers/${id}/reject/`, {});
  }

  getBookings(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/bookings/`, { params });
  }
}
