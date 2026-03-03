import { HttpClient } from "@angular/common/http";
import { inject, Injectable, signal } from "@angular/core";
import { Auth,authState,signOut } from "@angular/fire/auth";
import {Observable} from 'rxjs';
@Injectable({
  providedIn:'root',
})
export class AuthStateService{
  currentUser = signal<any>(null);
  private _auth = inject(Auth);
  private _http = inject(HttpClient);

private apiUrl = 'http://127.0.0.1:8000/api';

constructor() {
    // Firebase si alguien entra
    authState(this._auth).subscribe(user => {
      if (user) {
        // Si hay usuario en Firebase, pedimos sus datos a Django
        this.fetchUserProfile(user.uid);
      } else {
        // Si no hay usuario, limpiamos la señal
        this.currentUser.set(null);
      }
    });
  }
fetchUserProfile(uid: string) {
    this._http.get(`${this.apiUrl}/users/${uid}/`).subscribe({
      next: (userData) => {
        console.log('Datos traídos de Django:', userData);
        this.currentUser.set(userData); // se guardan los datos
      },
      error: (err) => console.error('Error obteniendo perfil de Django', err)
    });
  }
  get authState$():Observable<any>{
    return authState(this._auth);
  }
  logOut(){
    return signOut(this._auth);
  }
}
