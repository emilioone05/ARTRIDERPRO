import { Routes } from '@angular/router';
export default [
  {
    path: 'profile',
    loadComponent:()=> import('./profile-edit/profile-edit')
  }
] as Routes;
