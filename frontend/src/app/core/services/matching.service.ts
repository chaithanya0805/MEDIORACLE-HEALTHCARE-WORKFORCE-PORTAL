import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class MatchingService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8000/api/matches';

  getShiftMatches(shiftId: number) {
    return this.http.get<any>(`${this.baseUrl}/shift/${shiftId}/`);
  }

  generateShiftMatches(shiftId: number) {
    return this.http.post<any>(`${this.baseUrl}/shift/${shiftId}/generate/`, {});
  }
}
