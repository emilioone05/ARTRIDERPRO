// import { Injectable, inject } from '@angular/core';
// import { HttpClient, HttpParams } from '@angular/common/http';
// import { environment } from '../../../environments/environment';
// import { Observable } from 'rxjs';

// @Injectable({
//   providedIn: 'root'
// })
// export  class BookingService {
//   private http = inject(HttpClient);
//   private apiUrl = `${environment.apiUrl}/api/bookings/`; // Asegúrate que sea /bookings/

//   getReservations(isProviderMode: boolean): Observable<any[]> {
//     let params = new HttpParams();

//     if (isProviderMode) {
//       // Esto activa el "Serializer de Proveedor" en el Backend
//       params = params.set('mode', 'provider');
//     }

//     // Si no enviamos params, el Backend asume que es modo Cliente por defecto
//     return this.http.get<any[]>(this.apiUrl, { params });
//   }
//   updateReservationStatus(id: number, status: string): Observable<any> {
//   // PATCH es mejor para actualizaciones parciales
//   return this.http.patch(`${this.apiUrl}${id}/`, { status });
// }
// }
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';
import { PaginatedResponse } from '../models/reservation.model';

@Injectable({
  providedIn: 'root'
})
export class BookingService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/api/bookings/`;
  getReservations(isProviderMode: boolean): Observable<PaginatedResponse<any>> {
    let params = new HttpParams();

    if (isProviderMode) {
      params = params.set('mode', 'provider');
    }
    return this.http.get<PaginatedResponse<any>>(this.apiUrl, { params });
  }

  updateReservationStatus(id: number, status: string): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/`, { status });
  }
}
