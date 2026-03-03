
import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CatalogResponse } from '../interfaces/provider-dashboard.interface';
import { environment } from '../../../environments/environment';

export interface ProviderHomeStats {
  company_name: string;
  email: string;
  phone: string;
  location: string;
  published_equipments: number;
  active_reservations: number;
}

@Injectable({
  providedIn: 'root',
})
export class ProviderService {
  private http = inject(HttpClient);
  private apiUrl = environment.apiUrl;

  private catalogUrl = `${this.apiUrl}/api/inventory/provider/catalog/`;
  private homeUrl = `${this.apiUrl}/api/inventory/provider/home/`;

  getCatalogData(): Observable<CatalogResponse> {
    return this.http.get<CatalogResponse>(this.catalogUrl);
  }

  getHomeStats(): Observable<ProviderHomeStats> {
    return this.http.get<ProviderHomeStats>(this.homeUrl);
  }

  getPublicationById(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/api/publicaciones/${id}/`);
  }

  updatePublication(id: number, data: FormData): Observable<any> {
    return this.http.patch(`${this.apiUrl}/api/publicaciones/${id}/`, data);
  }

  createPublication(data: FormData): Observable<any> {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');

    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    return this.http.post(`${this.apiUrl}/api/publicaciones/`, data, { headers });
  }

  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/api/categories/`);
  }
  getMyPublications(): Observable<any> {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');

    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }

    // OPCIONAL: Si tu backend usa el mismo truco que en reservas,
    // podrías necesitar params = params.set('mode', 'provider');
    // Pero lo estándar es filtrar por el Token en el backend.

    return this.http.get(`${this.apiUrl}/api/publicaciones/`, { headers });
  }

  /**
   * Crea el paquete enviando el JSON con los items seleccionados.
   */
  createPackage(packageData: any): Observable<any> {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token');
    let headers = new HttpHeaders();
    if (token) headers = headers.set('Authorization', `Bearer ${token}`);

    // Asumimos que la ruta es /api/packages/ o ajusta según tu backend
    return this.http.post(`${this.apiUrl}/api/packages/`, packageData, { headers });
  }
}
