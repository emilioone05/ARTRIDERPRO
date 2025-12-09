import { Component, inject, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { toast, NgxSonnerToaster } from 'ngx-sonner';
import { AuthStateService } from './shared/data-acces/auth-state.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,NgxSonnerToaster],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {

}
