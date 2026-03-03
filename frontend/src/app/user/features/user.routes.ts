import { Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'profile-edit',
    loadComponent: () =>
      import('./profile-edit/profile-edit')
        .then(m => m.ProfileEditComponent)
  }
];

export default routes;
