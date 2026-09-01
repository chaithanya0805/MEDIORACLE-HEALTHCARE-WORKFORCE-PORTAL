import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MatchingService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/matches`;

  getShiftMatches(shiftId: number) {
    return this.http.get<any>(`${this.baseUrl}/shift/${shiftId}/`);
  }

  generateShiftMatches(shiftId: number) {
    return this.http.post<any>(`${this.baseUrl}/shift/${shiftId}/generate/`, {});
  }
}
