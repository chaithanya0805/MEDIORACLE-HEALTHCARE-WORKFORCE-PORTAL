import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface PaginatedResponse<T> {
  results: T[];
  count?: number;
  next?: string | null;
  previous?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class FacilityService {
  private http = inject(HttpClient);
  private baseUrl = 'https://medioracle-backend.onrender.com/api/facilities';

  getFacilities(): Observable<PaginatedResponse<any>> {
    return this.http.get<PaginatedResponse<any>>(`${this.baseUrl}/facilities/`);
  }

  getDepartments(facilityId?: number): Observable<PaginatedResponse<any>> {
    let params = new HttpParams();
    if (facilityId != null) {
      params = params.set('facility', facilityId.toString());
    }
    return this.http.get<PaginatedResponse<any>>(`${this.baseUrl}/departments/`, { params });
  }

  getWards(departmentId?: number): Observable<PaginatedResponse<any>> {
    let params = new HttpParams();
    if (departmentId != null) {
      params = params.set('department', departmentId.toString());
    }
    return this.http.get<PaginatedResponse<any>>(`${this.baseUrl}/wards/`, { params });
  }

  getRoles(): Observable<PaginatedResponse<any>> {
    return this.http.get<PaginatedResponse<any>>(`${this.baseUrl}/roles/`);
  }

  getSpecialties(roleId?: number): Observable<PaginatedResponse<any>> {
    let params = new HttpParams();
    if (roleId != null) {
      params = params.set('role', roleId.toString());
    }
    return this.http.get<PaginatedResponse<any>>(`${this.baseUrl}/specialties/`, { params });
  }
}
