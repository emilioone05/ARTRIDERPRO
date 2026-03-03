import { Component, inject } from "@angular/core";
import {  Router, RouterLink, RouterModule } from "@angular/router";
import { AuthStateService } from "../data-acces/auth-state.service";
import { NavbarComponent } from "./navbar";
import { FooterComponent } from "./footer";
@Component({
  standalone: true,
  imports: [RouterModule, NavbarComponent, FooterComponent],
  selector:'app-layout',
  template: `
  <app-navbar></app-navbar>
    <router-outlet/>
    <app-footer></app-footer>
  `,

})
export default class LayoutComponent{
  private _authState = inject(AuthStateService);
  private _router = inject(Router);
  async logOut(){
    await this._authState.logOut();
    this._router.navigateByUrl('/auth/sign-in')
  }
}
