import { Routes } from '@angular/router';
export default [
  {
    path: '',
    loadComponent:() => import('./home-page/home-page'),
  },
  {
    path:'new',
    loadComponent:()=> import('./dashboard/dashboard')
  }
] as Routes;
