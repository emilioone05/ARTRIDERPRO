import { inject, Injectable, signal } from '@angular/core';
import { Auth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signInWithPopup, GoogleAuthProvider,updatePassword,
  reauthenticateWithCredential,
  EmailAuthProvider } from '@angular/fire/auth';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';

export interface User {
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private _auth = inject(Auth);
  private http = inject(HttpClient);
  private apiUrl = 'http://127.0.0.1:8000/api';

  signUp(user: User) {
    return createUserWithEmailAndPassword(
      this._auth,
      user.email,
      user.password
    );
  }

  signIn(user: User) {
    return signInWithEmailAndPassword(
      this._auth,
      user.email,
      user.password
    );
  }

  signInWithGoogle() {
    const provider = new GoogleAuthProvider();
    return signInWithPopup(this._auth, provider);
  }

  // 5. Obtener los datos usando el UID real
  getProfile(): Observable<any> {
    const user = this._auth.currentUser;

    if (!user) return throwError(() => new Error('No usuario logueado'));

    return this.http.get(`${this.apiUrl}/users/${user.uid}/`);
  }

  updateProfile(data: any): Observable<any> {
    const user = this._auth.currentUser;
    if (!user) return throwError(() => new Error('No usuario logueado'));
    return this.http.patch(`${this.apiUrl}/users/${user.uid}/`, data);
  }

  //  Cambiar contraseña (requiere re-autenticación)
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    const user = this._auth.currentUser;

    if (!user || !user.email) {
      throw new Error('No hay usuario logueado o falta el email.');
    }

    try {

      const credential = EmailAuthProvider.credential(user.email, currentPassword);

      await reauthenticateWithCredential(user, credential);
      await updatePassword(user, newPassword);

    } catch (error: any) {
      // Manejo de errores comunes
      if (error.code === 'auth/wrong-password') {
        throw new Error('La contraseña actual es incorrecta.');
      }
      if (error.code === 'auth/too-many-requests') {
        throw new Error('Demasiados intentos fallidos. Intenta más tarde.');
      }
      throw error; // Relanzar otros errores para que los maneje el componente
    }
  }
}
