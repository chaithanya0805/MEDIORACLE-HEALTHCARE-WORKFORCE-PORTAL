import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ProfessionalService {
  private http = inject(HttpClient);
  private baseUrl = 'https://medioracle-backend.onrender.com/api/professionals';

  getProfiles(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/profiles/`, { params });
  }

  getProfile(id: number) {
    return this.http.get<any>(`${this.baseUrl}/profiles/${id}/`);
  }

  updateProfile(id: number, data: any) {
    return this.http.put<any>(`${this.baseUrl}/profiles/${id}/`, data);
  }

  createProfile(data: any) {
    return this.http.post<any>(`${this.baseUrl}/profiles/`, data);
  }

  getCredentials(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/credentials/`, { params });
  }

  getCredentialTypes() {
    return this.http.get<any>(`${this.baseUrl}/credential-types/`);
  }

  uploadCredential(data: FormData) {
    return this.http.post<any>(`${this.baseUrl}/credentials/`, data);
  }

  getCredentialDashboard() {
    return this.http.get<any>(`${this.baseUrl}/credentials/dashboard/`);
  }
}
