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
    // Lógica que se ejecuta al iniciar el componente
  }

  /**
   * Método para mostrar/ocultar un campo de búsqueda (si lo deseas implementar)
   */
  toggleSearch(): void {
    // Podrías usar esta función para mostrar un campo de búsqueda en el componente
    // o para navegar a una página de búsqueda.
    console.log('Botón de búsqueda clickeado. Implementa la lógica de búsqueda aquí.');
    // this.isSearchVisible = !this.isSearchVisible;
  }

  /**
   * Ejemplo de una función que podrías usar para navegar al hacer clic en un enlace.
   * Si usas Angular RouterLink, esto no es necesario.
   */
  // navigateTo(route: string): void {
  //   // Ejemplo de navegación con Router
  //   // this.router.navigate([route]);
  // }

}
