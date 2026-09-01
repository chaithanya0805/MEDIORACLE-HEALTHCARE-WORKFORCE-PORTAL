import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/analytics`;

  getFacilityAnalytics() {
    return this.http.get<any>(`${this.baseUrl}/facility/`);
  }

  getAgencyAnalytics() {
    return this.http.get<any>(`${this.baseUrl}/agency/`);
  }

  simulateWhatIf(censusChangePct: number) {
    return this.http.post<any>(`${this.baseUrl}/what-if/`, { census_change: censusChangePct });
  }
}
