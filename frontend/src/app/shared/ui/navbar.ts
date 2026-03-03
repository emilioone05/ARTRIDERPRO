import { Component, inject, computed, signal, OnInit } from '@angular/core'; // Añadí OnInit que faltaba en imports
import { NavigationEnd, Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthStateService } from '../data-acces/auth-state.service';
import { CommonModule } from '@angular/common';
import { filter } from 'rxjs';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, CommonModule],
  template: `
    <header class="sticky top-4 z-50">
      <nav
        class="liquid-glass max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between"
      >
        <a routerLink="/home/new" class="flex items-center gap-2 cursor-pointer select-none">
          <div
            class="w-10 h-10 rounded-full border-2 border-black flex items-center justify-center"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"
              />
            </svg>
          </div>
          <span class="text-xl font-bold text-gray-900 tracking-tight">ArtRider</span>
        </a>

        <div class="hidden md:flex items-center gap-6 font-medium text-gray-950">
          @if (!isProviderMode()) {
          <a
            routerLink="/equipos"
            routerLinkActive="text-black font-semibold bg-white/40 shadow-sm"
            class="px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-300"
          >
            Equipos
          </a>
          <a
            routerLink="/paquetes"
            routerLinkActive="text-black font-semibold bg-white/40 shadow-sm"
            class="px-4 py-2 rounded-full hover:bg-white/20 transition-all duration-300"
          >
            Paquetes
          </a>
          } @else {
          <a
            routerLink="/provider/catalog"
            routerLinkActive="text-purple-900 font-bold bg-purple-100 shadow-sm"
            class="px-4 py-2 rounded-full hover:bg-white/20 text-purple-900 transition-all duration-300 flex items-center gap-2"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-5 h-5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13.5 21v-7.5a.75.75 0 0 1 .75-.75h3a.75.75 0 0 1 .75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 0 0 3.75-.615A2.993 2.993 0 0 0 9.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 0 0 2.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 0 0 3.75.614m-16.5 0a3.004 3.004 0 0 1-.621-4.72l1.189-1.19A1.5 1.5 0 0 1 5.378 3h13.243a1.5 1.5 0 0 1 1.06.44l1.19 1.189a3 3 0 0 1-.621 4.72m-13.5 8.65h3.75a.75.75 0 0 0 .75-.75V13.5a.75.75 0 0 0-.75-.75H6.75a.75.75 0 0 0-.75.75v3.75c0 .415.336.75.75.75Z"
              />
            </svg>
            <span>Mi Catálogo</span>
          </a>
          }

          <a
            [routerLink]="isProviderMode() ? '/provider/reservas' : '/reservas'"
            [routerLinkActive]="
              isProviderMode()
                ? 'text-purple-900 font-bold bg-purple-100 shadow-sm'
                : 'text-black font-semibold bg-white/40 shadow-sm'
            "
            [ngClass]="
              isProviderMode()
                ? 'text-purple-900 hover:bg-white/20'
                : 'text-gray-950 hover:bg-white/20'
            "
            class="px-4 py-2 rounded-full transition-all duration-300 cursor-pointer"
          >
            Mis Reservas
          </a>

          @if (isProviderMode()) {
          <a
            routerLink="/provider/home"
            routerLinkActive="text-purple-900 font-bold bg-purple-100 shadow-sm"
            class="px-4 py-2 rounded-full hover:bg-white/20 text-purple-900 transition-all duration-300"
          >
            Panel de Proveedor
          </a>
          } @if (userRole() === 'proveedor') {
          <div class="flex items-center gap-3 ml-4 pl-4 border-l border-gray-300">
            <span
              class="text-sm font-semibold text-gray-700 select-none cursor-pointer"
              (click)="toggleProviderMode()"
            >
              Modo proveedor
            </span>

            <button
              (click)="toggleProviderMode()"
              class="relative w-12 h-7 rounded-full transition-colors duration-300 focus:outline-none shadow-inner"
              [ngClass]="isProviderMode() ? 'bg-purple-900' : 'bg-gray-300'"
            >
              <div
                class="absolute top-1 left-1 bg-white w-5 h-5 rounded-full shadow-md transform transition-transform duration-300 flex items-center justify-center"
                [ngClass]="isProviderMode() ? 'translate-x-5' : 'translate-x-0'"
              >
                @if (isProviderMode()) {
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  class="w-3.5 h-3.5 text-purple-900"
                >
                  <path
                    fill-rule="evenodd"
                    d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z"
                    clip-rule="evenodd"
                  />
                </svg>
                }
              </div>
            </button>
          </div>
          }
        </div>

        <div class="flex items-center gap-6">
          @if (!isProviderMode()) {
          <button
            class="hidden md:block text-sm font-medium text-gray-950 px-4 py-2 rounded-full hover:bg-white/20 backdrop-blur-md transition group relative"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="1.5"
              stroke="currentColor"
              class="w-6 h-6 group-hover:text-black"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
              />
            </svg>
            @if (cartCount() > 0) {
            <span
              class="absolute top-1 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full"
            >
              {{ cartCount() }}
            </span>
            }
          </button>
          }

          <div class="relative">
            <button
              (click)="toggleMenu()"
              class="flex items-center gap-2 border border-gray-300 rounded-full pl-3 pr-1 py-1 hover:shadow-md transition-shadow bg-white"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.5"
                stroke="currentColor"
                class="w-5 h-5 text-gray-600"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                />
              </svg>
              <div class="bg-gray-500 text-white rounded-full p-1">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 24 24"
                  fill="currentColor"
                  class="w-5 h-5"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.5 6a4.5 4.5 0 1 1 9 0 4.5 4.5 0 0 1-9 0ZM3.751 20.105a8.25 8.25 0 0 1 16.498 0 .75.75 0 0 1-.437.695A18.683 18.683 0 0 1 12 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 0 1-.437-.695Z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
            </button>

            @if (isMenuOpen) {
            <div
              class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50 overflow-hidden animate-fade-in-down"
            >
              <a
                routerLink="/user/profile-edit"
                (click)="isMenuOpen = false"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-900"
              >
                Mi Perfil
              </a>

              @if (userRole() === 'proveedor') {
              <a
                routerLink="/provider/settings"
                (click)="isMenuOpen = false"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-black"
              >
                Configuración de Negocio
              </a>
              }

              <div class="h-px bg-gray-100 my-1"></div>
              <button
                (click)="logOut()"
                class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
              >
                Cerrar sesión
              </button>
            </div>
            }
          </div>
        </div>
      </nav>
    </header>
  `,
})
export class NavbarComponent implements OnInit {
  isMenuOpen = false;
  isProviderMode = signal<boolean>(false);

  private _authState = inject(AuthStateService);
  private _router = inject(Router);

  userRole = computed(() => {
    const user = this._authState.currentUser();
    return user?.account_type || 'cliente';
  });

  cartCount = signal<number>(0);

  ngOnInit() {
    this.checkUrlForProviderMode();

    this._router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
      this.checkUrlForProviderMode();
    });
  }

  private checkUrlForProviderMode() {
    const isProviderUrl = this._router.url.includes('/provider');
    this.isProviderMode.set(isProviderUrl);
  }
  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  toggleProviderMode() {
    this.isProviderMode.update((val) => !val);
    if (this.isProviderMode()) {
      this._router.navigate(['/provider/home']);
    } else {
      this._router.navigate(['/home/new']);
    }
  }

  async logOut() {
    await this._authState.logOut();
    this._router.navigateByUrl('/auth/sign-in');
  }
}
