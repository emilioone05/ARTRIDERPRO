import { Routes } from '@angular/router';
import { privateGuard, publicGuard } from './core/auth.guard';
import { CatalogComponent } from './provider/features/catalog/catalog';
import { EditEquipmentComponent } from './provider/features/catalog/edit-equipment/edit-equipment';
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
  {
    // AL ESTAR DENTRO DE ESTE BLOQUE, HEREDA EL LAYOUT Y LA PROTECCIÓN
    path: 'provider',
    canActivateChild: [privateGuard()],
    loadComponent: () => import('./shared/ui/layout'),
    loadChildren: () => import('./provider/provider.routes').then(m => m.providerRoutes)
  },
  {
    path: 'reservas',
    canActivate: [privateGuard()], // Protegemos la entrada
    loadComponent: () => import('./shared/ui/layout'), // Cargamos el Navbar
    children: [
      {
        path: '',
        loadComponent: () => import('./provider/features/booking/provider-reservas').then(m => m.ProviderReservationsComponent)
      }
    ]
  },
  {
    path: 'provider',
    canActivateChild: [privateGuard()],
    loadComponent: () => import('./shared/ui/layout'),
    // Aquí dentro cargamos provider.routes
    loadChildren: () => import('./provider/provider.routes').then(m => m.providerRoutes)
  },
  // {
  //   path: 'reservas',
  //   loadComponent:() => import('./provider/features/booking/provider-reservas'),
  //   loadChildren
  // }



];
