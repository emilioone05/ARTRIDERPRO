import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router'; // ◄◄◄ ¡1. IMPORTAR LA CLASE!

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, 
    RouterOutlet // ◄◄◄ ¡2. DECLARAR EN IMPORTS!
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class AppComponent {
  title = 'artrider-front';
}