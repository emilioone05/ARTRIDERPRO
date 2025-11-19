// import { Component } from '@angular/core';
// import { CommonModule } from '@angular/common';
// import { AuthService } from '../../services/auth';
// import { Router } from '@angular/router';

// @Component({
//   selector: 'app-home',
//   standalone: true,
//   imports: [CommonModule],
//   templateUrl: './home.html',
//   styleUrls: ['./home.css']
// })
// export class HomeComponent {
//   constructor(
//     private authService: AuthService,
//     private router: Router
//   ) {}

//   // Creamos un método para cerrar sesión
//   async onLogout(): Promise<void> {
//     try {
//       await this.authService.logout();
//       // Si el logout es exitoso, redirigimos al login
//       this.router.navigate(['/login']);
//     } catch (error) {
//       console.error('Error al cerrar sesión:', error);
//       // Aquí podrías mostrar un mensaje de error si falla
//     }
//   }
// }
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent implements OnInit {
  isSearchVisible: boolean = false;

  constructor() { }

  ngOnInit(): void {
  }

  /**
   * Método para mostrar/ocultar un campo de búsqueda (si lo deseas implementar)
   */
  toggleSearch(): void {
    console.log('Botón de búsqueda clickeado. Implementa la lógica de búsqueda aquí.');
    // this.isSearchVisible = !this.isSearchVisible;
  }


}
