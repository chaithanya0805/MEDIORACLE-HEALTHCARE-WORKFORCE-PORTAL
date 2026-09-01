import { inject, Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

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
  private baseUrl = `${environment.apiUrl}/facilities`;

  getFacilities(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/facilities/`);
  }

  getDepartments(facilityId?: number): Observable<any> {
    let params = new HttpParams();
    if (facilityId != null) {
      params = params.set('facility', facilityId.toString());
    }
    return this.http.get<any>(`${this.baseUrl}/departments/`, { params });
  }

  getWards(departmentId?: number): Observable<any> {
    let params = new HttpParams();
    if (departmentId != null) {
      params = params.set('department', departmentId.toString());
    }
    return this.http.get<any>(`${this.baseUrl}/wards/`, { params });
  }

  getRoles(): Observable<any> {
    return this.http.get<any>(`${this.baseUrl}/roles/`);
  }

  getSpecialties(roleId?: number): Observable<any> {
    let params = new HttpParams();
    if (roleId != null) {
      params = params.set('role', roleId.toString());
    }
    return this.http.get<any>(`${this.baseUrl}/specialties/`, { params });
  }
}
