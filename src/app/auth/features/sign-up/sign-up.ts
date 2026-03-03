import { Component, inject } from '@angular/core';
import {AbstractControl,FormBuilder, FormControl, ReactiveFormsModule, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import { hasEmailError, isRequired } from '../../utils/validatos';
import { AuthService } from '../../data-access/auth';
import { toast } from 'ngx-sonner';
import { Router, RouterLink } from '@angular/router';
import { GoogleButton } from '../../ui/google-button/google-button';
import { first } from 'rxjs';
import { HttpClient } from '@angular/common/http';
interface FormSignUp{
  full_name: FormControl<string|null>
  // first_name: FormControl<string| null>;
  // last_name: FormControl<string| null>;
  email: FormControl<string| null>;
  phone_number: FormControl<string| null>;
  password: FormControl<string| null>;
  confirmPassword: FormControl<string | null>;
  typeAccount:FormControl<string|null>;
}
const passwordMatchValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const password = control.get('password')?.value;
  const confirmPassword = control.get('confirmPassword')?.value;

  if (!password || !confirmPassword) {
    return null;
  }

  return password === confirmPassword ? null : { passwordMismatch: true };
};

@Component({
  selector: 'app-sign-up',
  imports: [ReactiveFormsModule,RouterLink,GoogleButton],
  templateUrl: './sign-up.html',
  styles: ``,
})
export default class SignUp {
  private _formBuilder = inject(FormBuilder);
  private _authService = inject(AuthService);
  private _router = inject(Router);
  private _http = inject(HttpClient);

  private apiUrl = 'http://127.0.0.1:8000/api';


  isRequired(field: 'email' | 'password'|'phone_number' ){
      return isRequired(field,this.form);
  }

  hasEmailRequired(){
    return hasEmailError(this.form);
  }

  // hasPasswordMismatch() {
  //   return this.form.get('confirmPassword')?.hasError('passwordMismatch') &&
  //          this.form.get('confirmPassword')?.touched;
  // }
  hasPasswordMismatch() {
  return this.form.hasError('passwordMismatch') &&
         this.form.get('confirmPassword')?.touched;
}


  form = this._formBuilder.group<FormSignUp>({

    full_name:this._formBuilder.control('',Validators.required),
    // first_name:this._formBuilder.control('',Validators.required),
    // last_name:this._formBuilder.control('',Validators.required),
    email:this._formBuilder.control('',[
      Validators.required,
      Validators.email]),
    phone_number: this._formBuilder.control('', [
      Validators.required,
      Validators.pattern('^[0-9]*$')]),
    password:this._formBuilder.control('',Validators.required),
    confirmPassword: this._formBuilder.control('', Validators.required),
    typeAccount: new FormControl('cliente', Validators.required),
  },{ validators: passwordMatchValidator });

  async submit(){
    console.log("Botón presionado...");

  if (this.form.invalid) {
      console.log("FORMULARIO INVÁLIDO. Errores:", this.form.errors);

      Object.keys(this.form.controls).forEach(key => {
          const errors = this.form.get(key)?.errors;
          if (errors) {
              console.log(`El campo '${key}' tiene error:`, errors);
          }
      });

      this.form.markAllAsTouched();
      return;
  }

    try {
      const{full_name,email,phone_number,password,typeAccount} = this.form.value;

    if(!full_name||!email||! phone_number || !password|| !typeAccount) return;

    const firebaseCredential =await this._authService.signUp({email,password});
    const firebaseUid = firebaseCredential.user?.uid;

    const backendData = {
        // username: firebaseUid,
        email: email,
        phone_number:phone_number,
        full_name:full_name,
        account_type: typeAccount,
        firebase_uid: firebaseUid,
      };
      console.log('Tipo de cuenta seleccionado:', typeAccount);

      this._http.post(`${this.apiUrl}/users/`, backendData)
        .subscribe({
            next: (response) => {
                toast.success('Usuario creado y perfil guardado correctamente');
                this._router.navigateByUrl('/home/new');
            },
            error: (err) => {
                console.error('Error en Django',err);
                toast.warning('Cuenta creada pero ERROR al guardar')
                toast.error('Se creó en Firebase pero falló al guardar en la base de datos.');

            }
        });

    } catch (error: any) {

      if(error.code === 'auth/email-already-in-use'){
          toast.error('El correo ya está registrado');
      } else {
          toast.error('Ocurrió un error al registrarse');
      }
    }
  }

async submitWithGoogle() {
  try {
    const credential = await this._authService.signInWithGoogle();
    const user = credential.user;

    //  obtener el perfil
    this._http.get(`${this.apiUrl}/users/${user.uid}/`).subscribe({
      next: () => {

        toast.success(`Bienvenido de nuevo ${user.displayName}`);
        this._router.navigateByUrl('/home');
      },
      error: (err) => {
        if (err.status === 404) {
          console.log("Usuario no encontrado, creando perfil...");

          const newGoogleUser = {
            email: user.email,
            full_name: user.displayName || 'Usuario Google',
            phone_number: user.phoneNumber || '',
            account_type: 'cliente',
            firebase_uid: user.uid
          };

          this._http.post(`${this.apiUrl}/users/`, newGoogleUser).subscribe({
            next: () => {
              toast.success('Cuenta vinculada con éxito');
              this._router.navigateByUrl('/home');
            },
            error: (createErr) => {
              console.error('Error creando perfil:', createErr);
              toast.error('Error al guardar el perfil en la base de datos');
            }
          });
        } else {
          console.error('Error inesperado:', err);
          toast.error('Error de conexión con el servidor');
        }
      }
    });
  } catch (error) {
    toast.error('Error con Google');
  }
}
}
