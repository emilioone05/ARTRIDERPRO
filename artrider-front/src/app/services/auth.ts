import { Injectable, inject } from '@angular/core';
import {
  Auth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  authState
} from '@angular/fire/auth';
import {
  Firestore,
  doc,
  setDoc
} from '@angular/fire/firestore';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // --- Inyecciones ---
  private auth: Auth = inject(Auth);
  // ======================================
  // == PASO 2: INYECTA FIRESTORE ==
  // ======================================
  private firestore: Firestore = inject(Firestore);

  readonly authState = authState(this.auth);

  constructor() { }

  // --- Métodos de Auth  ---

  // Registrar a los pilinsitos
  register(email: string, password: string) {

    return createUserWithEmailAndPassword(this.auth, email, password);
  }

  // Iniciar Sesión a los aghrider
  login(email: string, password: string) {
    // Quitamos el 'from()'
    return signInWithEmailAndPassword(this.auth, email, password);
  }

  // Cerrar Sesión putitos
  logout() {
    return signOut(this.auth);
  }
  // AQUI SE GUARDA LOS ADTOS ADICIONALES como el rol
  saveUserData(uid: string, data: any) {
    const userDocRef = doc(this.firestore, `users/${uid}`);

    // Guarda el documento ania
    return setDoc(userDocRef, data);
  }
}
