import { Routes } from '@angular/router';
import { privateGuard, publicGuard } from './core/auth.guard';

export const routes: Routes = [
  {
    canActivateChild:[publicGuard()],
    path: 'auth',
    loadChildren: ()=> import('./auth/features/auth.routes')
  },
  {
    path: 'equipment',
    loadChildren: ()=> import ('./equipment/features/equipment.routes')
  },
  {
    canActivateChild:[privateGuard()],
    path: 'home',
    loadComponent:()=> import('./shared/ui/layout'),

    loadChildren: ()=> import('./home/features/home.routes'),


  },
  {
    canActivateChild:[privateGuard()],
    path:'user',
    loadChildren:()=> import('./user/features/user.routes'),
  },



];
