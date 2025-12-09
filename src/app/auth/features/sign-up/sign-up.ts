import { Component, inject } from '@angular/core';
import {FormBuilder, FormControl, ReactiveFormsModule, Validators} from '@angular/forms';
import { hasEmailError, isRequired } from '../../utils/validatos';
import { AuthService } from '../../data-access/auth';
import { toast } from 'ngx-sonner';
import { Router, RouterLink } from '@angular/router';
import { GoogleButton } from '../../ui/google-button/google-button';
interface FormSignUp{
  name: FormControl<string| null>;
  email: FormControl<string| null>;
  password: FormControl<string| null>;
  typeAccount:FormControl<string|null>;
}
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
  isRequired(field: 'email' | 'password'){
      return isRequired(field,this.form);
  }
  hasEmailRequired(){
    return hasEmailError(this.form);
  }
  form = this._formBuilder.group<FormSignUp>({
    name:this._formBuilder.control('',Validators.required),
    email:this._formBuilder.control('',[
      Validators.required,
      Validators.email]),
    password:this._formBuilder.control('',Validators.required),
    typeAccount: new FormControl('cliente', Validators.required),

  });
  async submit(){
    if(this.form.invalid ) return;
    try {
      const{name,email,password} = this.form.value;

    if(!name||!email || !password) return;

    await this._authService.signUp({email,password});

    toast.success('Usuario Creado correctamente')

    this._router.navigateByUrl('/home')
    } catch (error) {
      toast.error('Ocurrio un error')
    }
  }
  async submitWithGoogle(){
    try {
      await this._authService.signInWithGoogle();
      toast.success("Bienvenido de nuevo")
      this._router.navigateByUrl('/home')
    } catch (error) {
      toast.error('Ocurrio un error')
    }
  }
}

// onSubmit() {
//     if (this.form.valid) {
//       console.log('Formulario válido:', this.form.value);
//       // Resultado esperado: { name: '...', email: '...', typeAccount: 'cliente' | 'proveedor', ... }

//       const tipoDeCuenta = this.form.value.typeAccount;
//       if (tipoDeCuenta === 'proveedor') {
//          console.log('Registrando como proveedor...');
//       } else {
//          console.log('Registrando como cliente...');
//       }
//     } else {
//       this.form.markAllAsTouched(); // Marca campos en rojo si hay error
//     }
//   }
// }
