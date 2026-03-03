import { Routes } from '@angular/router';
export default [
  {
    path: 'sign-in',
    loadComponent:() => import('./sign-in/sign-in'),
  },
  {
    path: 'sign-up',
    loadComponent:() => import('./sign-up/sign-up'),
  }
] as Routes
