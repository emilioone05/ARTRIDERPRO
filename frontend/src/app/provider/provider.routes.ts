  import { Routes } from '@angular/router';
  import { HomeComponent } from './features/home/home';
  import { CatalogComponent} from './features/catalog/catalog';
  import { EditEquipmentComponent } from './features/catalog/edit-equipment/edit-equipment'; // Importa el componente aquí
  import { PublishEquipmentComponent } from './features/catalog/publish-equipment/publish-equipment';
  import { PublishPackageComponent } from './features/catalog/publish-package/publish-package';
  export const providerRoutes: Routes = [
    {
      path: '',
      redirectTo: 'home',
      pathMatch: 'full'
    },
    {
      path: 'home',      //  /provider/home
      component: HomeComponent
    },
    {
      path: 'catalog',   // /provider/catalog
      component: CatalogComponent
    },
    {
    path: 'provider',
    redirectTo: 'catalog',
    pathMatch: 'full'
  },
  {
    path: 'catalog/publish', // Ruta para publicar
    component: PublishEquipmentComponent
  },
  {
    path: 'catalog/publish-package', // Ruta para publicar
    component: PublishPackageComponent
  },
  {
    // Solo ponemos 'catalog/edit/:id' porque 'provider/' ya lo pone el padre
    path: 'catalog/edit/:id',
    component: EditEquipmentComponent
  },
  {
    path: 'reservas', // Esto crea: /provider/reservas
    loadComponent: () => import('./features/booking/provider-reservas').then(m => m.ProviderReservationsComponent)
  },

  ];
