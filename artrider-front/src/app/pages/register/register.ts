// import { Component, ChangeDetectionStrategy } from '@angular/core';
// import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
// import { Router, RouterLink } from '@angular/router';
// import { CommonModule } from '@angular/common';
// import { AuthService } from '../../services/auth';

// @Component({
//   selector: 'app-register',
//   standalone: true,
//   imports: [
//     CommonModule,
//     ReactiveFormsModule,
//     RouterLink
//   ],
//   templateUrl: './register.html',
//   styleUrls: ['./register.css'],
//   changeDetection: ChangeDetectionStrategy.OnPush
// })
// export class RegisterComponent {
//   registerForm: FormGroup;
//   errorMessage: string | null = null;

//   constructor(
//     private fb: FormBuilder,
//     private authService: AuthService,
//     private router: Router
//   ) {
//     this.registerForm = this.fb.group({
//       email: ['', [Validators.required, Validators.email]],
//       password: ['', [Validators.required, Validators.minLength(6)]]
//     });
//   }

//   async onSubmit(): Promise<void> {
//     if (this.registerForm.invalid) { return; }
//     this.errorMessage = null;

//     const { email, password } = this.registerForm.value;

//     try {
//       await this.authService.register(email, password);
//       // Si el registro es exitoso, lo mandamos al login
//       this.router.navigate(['/login']);

//     } catch (error: any) {
//       if (error.code === 'auth/email-already-in-use') {
//         this.errorMessage = 'Este email ya está en uso.';
//       } else {
//         this.errorMessage = 'Ocurrió un error al registrarse.';
//       }
//     }
//   }
// }
import { Component, ChangeDetectionStrategy } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  Validators,
  ReactiveFormsModule,
  AbstractControl,
  ValidationErrors,
  ValidatorFn
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../services/auth';

// ======================================
// == VALIDACIÓN DE CONTRASEÑAS IGUALES ==
// ======================================
export const passwordMatchValidator: ValidatorFn = (
  control: AbstractControl
): ValidationErrors | null => {
  const password = control.get('password');
  const confirmPassword = control.get('confirmPassword');

  // Si los campos no coinciden, devuelve un error
  if (password && confirmPassword && password.value !== confirmPassword.value) {
    return { passwordMismatch: true };
  }

  return null;
};


@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './register.html',
  styleUrls: ['./register.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class RegisterComponent {
  registerForm: FormGroup;
  errorMessage: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      // ======================================
      // == CAMPOS DEL FORMULARIO COMPLETOS ==
      // ======================================
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]], 

      // Campos extra del formulario
      name: ['', [Validators.required]],
      phone: ['', [Validators.required]],
      dob: ['', [Validators.required]],
      role: ['cliente', [Validators.required]] // ESTO ES POR DEFECTO, que es cliente 
    }, {
      // ======================================
      // == APLICAR EL VALIDADOR AL GRUPO ==
      // ======================================
      validators: passwordMatchValidator
    });
  }

  async onSubmit(): Promise<void> {
    this.errorMessage = null;

    // ======================================
    // == VALIDACIÓN ANTES DE ENVIAR ==
    // ======================================
    if (this.registerForm.invalid) {

      // Chequeo específico para el error de contraseñas
      if (this.registerForm.errors?.['passwordMismatch']) {
        this.errorMessage = 'Las contraseñas no coinciden.';
      } else {
        // Mensaje si falta otro campo
        this.errorMessage = 'Por favor, completa todos los campos requeridos.';
      }
      return; 
    }

    // Obtenemos todos los valores del formulario
    const { email, password, name, phone, dob, role } = this.registerForm.value;

    try {
      // ======================================
      // == PASO 1: Crear usuario en Auth ==
      // ======================================
      const userCredential = await this.authService.register(email, password);

      const uid = userCredential.user.uid;
// DATOS EXTRA
      const userData = {
        email,
        name,
        phone,
        dob,
        role,
        createdAt: new Date() 
      };

      // ======================================
      // == PASO 3: Guardar datos en Firestore ==
      // ======================================
      // 
      await this.authService.saveUserData(uid, userData);

      // LO MANDO AL LOGIN 
      this.router.navigate(['/login']);

    } catch (error: any) {
      // ======================================
      // == MANEJO DE ERRORES DE FIREBASE ==
      // ======================================
      if (error.code === 'auth/email-already-in-use') {
        this.errorMessage = 'Este email ya está en uso.';
      } else {
        console.error(error); 
        this.errorMessage = 'Ocurrió un error inesperado al registrarse.';
      }
    }
  }
}
