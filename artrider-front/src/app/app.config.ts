import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

// --- Firebase ---
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { getAuth, provideAuth } from '@angular/fire/auth';

// ======================================
// == PASO 1: IMPORTA FIRESTORE AQUÍ ==
// ======================================
import { getFirestore, provideFirestore } from '@angular/fire/firestore';


export const appConfig: ApplicationConfig = {

  providers: [
    provideRouter(routes),
    provideHttpClient(),
    // FIREBASE
    provideFirebaseApp(() => initializeApp(environment.firebase)),
   
    //Cargar los servicios de Firebase (que dependen de la App)
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore())
  ]
};
