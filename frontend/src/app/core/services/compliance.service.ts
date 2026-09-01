import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ComplianceService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/compliance`;

  checkCompliance(professionalId: number, shiftId: number) {
    return this.http.post<any>(`${this.baseUrl}/check/`, {
      professional_id: professionalId,
      shift_id: shiftId
    });
  }

  getRules(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/rules/`, { params });
  }
}
