import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  provideZoneChangeDetection,
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { initializeApp, provideFirebaseApp } from '@angular/fire/app';
import { getAuth, provideAuth } from '@angular/fire/auth';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideFirebaseApp(() =>
      initializeApp({
        projectId: 'artrider2',
        appId: '1:210207273877:web:ce0de7837f7c07ce7dbc9c',
        storageBucket: 'artrider2.firebasestorage.app',
        apiKey: 'AIzaSyCfjQNu8i-xuUjW1a3pOitoXd5G66MMPTc',
        authDomain: 'artrider2.firebaseapp.com',
        messagingSenderId: '210207273877',
        measurementId: 'G-5VEL2NPR2V',
      })
    ),
    provideAuth(() => getAuth()),
  ],
};
