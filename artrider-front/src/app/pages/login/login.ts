import { Component, ChangeDetectionStrategy } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { AuthService } from '../../services/auth';
import { Router, RouterLink } from '@angular/router'; // Para redirigir
import { CommonModule } from '@angular/common'; // Para *ngIf

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router // Inyectamos el Router
  ) {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required]]
    });
  }

  async onSubmit(): Promise<void> {
    if (this.loginForm.invalid) { return; }
    this.errorMessage = null;

    // Separamos email y password para pasarlos al servicio
    const { email, password } = this.loginForm.value;

    try {
      // Llamamos al servicio
      await this.authService.login(email, password);

      // Si todo sale bien, redirigimos al usuario
      this.router.navigate(['/']); // <-- Puedes cambiar '/' por '/dashboard' o '/home'

    } catch (error: any) {
      // Si Firebase da un error, lo mostramos
      this.errorMessage = 'Email o contraseña incorrectos.';
    }
  }
}
