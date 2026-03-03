import { Routes } from '@angular/router';
export default [
  {
    path: '',
    loadComponent:() => import('./equipment-list/equipment-list'),
  }
] as Routes
