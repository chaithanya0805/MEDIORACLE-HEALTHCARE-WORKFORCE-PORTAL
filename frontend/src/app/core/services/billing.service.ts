import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BillingService {
  private http = inject(HttpClient);
  private baseUrl = `${environment.apiUrl}/billing`;

  getInvoices(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/invoices/`, { params });
  }

  getPayments(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/payments/`, { params });
  }

  processPayment(paymentId: number) {
    return this.http.post<any>(`${this.baseUrl}/payments/${paymentId}/process_payment/`, {});
  }

  getDisputes(params?: any) {
    return this.http.get<any>(`${this.baseUrl}/disputes/`, { params });
  }

  createDispute(data: any) {
    return this.http.post<any>(`${this.baseUrl}/disputes/`, data);
  }

  resolveDispute(disputeId: number, resolution: string) {
    return this.http.post<any>(`${this.baseUrl}/disputes/${disputeId}/resolve/`, { resolution });
  }
}
