import { Component, inject } from '@angular/core';
import {FormBuilder, FormControl, ReactiveFormsModule, Validators} from '@angular/forms';
import { hasEmailError, isRequired } from '../../utils/validatos';
import { AuthService } from '../../data-access/auth';
import { toast } from 'ngx-sonner';
import { Router, RouterLink } from '@angular/router';
import { GoogleButton } from '../../ui/google-button/google-button';

export interface FormSignIn{
  email: FormControl<string| null>;
  password: FormControl<string| null>;
}
@Component({
  selector: 'app-sign-in',
  imports: [ReactiveFormsModule,RouterLink,GoogleButton],
  templateUrl: './sign-in.html',
  styles: ``,
})
export default class SignIn {
  private _formBuilder = inject(FormBuilder);
  private _authService = inject(AuthService);
  private _router = inject(Router);
  isRequired(field: 'email' | 'password'){
      return isRequired(field,this.form);
  }
  hasEmailRequired(){
    return hasEmailError(this.form);
  }
  form = this._formBuilder.group<FormSignIn>({
    email:this._formBuilder.control('',[
      Validators.required,
      Validators.email]),
    password:this._formBuilder.control('',Validators.required),
  });
  async submit(){
    if(this.form.invalid ) return;
    try {
      const{email,password} = this.form.value;

    if(!email || !password) return;

    await this._authService.signIn  ({email,password});

    toast.success('Bienvenido a artrider')

    this._router.navigateByUrl('/home/new')
    } catch (error) {
      toast.error('Ocurrio un error')
    }
  }
  async submitWithGoogle(){
    try {
      await this._authService.signInWithGoogle();
      toast.success("Bienvenido de nuevo")
      this._router.navigateByUrl('/home/new')

    } catch (error) {
      toast.error('Ocurrio un error')
    }
  }
}
