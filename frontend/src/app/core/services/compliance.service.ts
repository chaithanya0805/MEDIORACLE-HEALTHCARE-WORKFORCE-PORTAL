import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ComplianceService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api/compliance';

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
