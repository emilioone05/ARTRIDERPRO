import { Component, OnInit, inject } from '@angular/core';
import { CommonModule ,Location} from '@angular/common';
import { AbstractControl, FormBuilder, FormGroup, ValidationErrors, ValidatorFn, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { toast } from 'ngx-sonner';
import { AuthService } from '../../../auth/data-access/auth';

const passwordMatchValidator: ValidatorFn = (control: AbstractControl): ValidationErrors | null => {
  const password = control.get('newPassword');
  const confirmPassword = control.get('confirmPassword');
  return password && confirmPassword && password.value !== confirmPassword.value ? { passwordMismatch: true } : null;
};
@Component({
  selector: 'app-profile-edit',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule ],
  templateUrl: './profile-edit.html',
  styles: ``
})
export class ProfileEditComponent implements OnInit {
  private _location = inject(Location);
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  activeTab: string = 'personal';

  profileForm: FormGroup;
  securityForm: FormGroup;
  loading = false;

  // Datos personales
  headerInfo = {
    name: '',
    email: '',
    initial: ''
  };

  constructor() {
    // formulario
    this.profileForm = this.fb.group({
      full_name: ['', [Validators.required, Validators.minLength(3)]],
      email: [{ value: '', disabled: true }],
      role: [{ value: '', disabled: true }]
    });

    this.securityForm = this.fb.group({
      currentPassword: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    }, { validators: passwordMatchValidator });
  }
  goBack() {
    this._location.back();
  }
  ngOnInit(): void {
    this.loadData();
  }

  loadData() {
    this.loading = true;

    this.authService.getProfile().subscribe({
      next: (userProfile: any) => {

        const rawRole = userProfile.account_type || 'cliente';
        const formattedRole = rawRole.charAt(0).toUpperCase() + rawRole.slice(1);

        // Rellenar el formulario con los datos de la BD
        this.profileForm.patchValue({
          full_name: userProfile.full_name || '',
          email: userProfile.email,
          role: formattedRole
        });

        // Actualizar datos personales
        this.updateHeaderInfo(userProfile.full_name, userProfile.email);

        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando perfil:', err);
        toast.error('No se pudo cargar la información del perfil');
        this.loading = false;
      }
    });
  }

  onSubmit() {
    if (this.profileForm.valid) {
      this.loading = true;

      // Preparamos solo los datos que se pueden editar
      const formData = {
        full_name: this.profileForm.get('full_name')?.value
      };

      this.authService.updateProfile(formData).subscribe({
        next: (res: any) => {
          toast.success('Perfil actualizado correctamente');
          this.loading = false;

          // Actualizamos la cabecera visualmente sin recargar
          this.updateHeaderInfo(res.full_name, this.headerInfo.email);
        },
        error: (err) => {
          console.error(err);
          toast.error('Error al guardar los cambios');
          this.loading = false;
        }
      });
    } else {
      this.profileForm.markAllAsTouched();
    }
  }
  onSecuritySubmit() {
    if (this.securityForm.valid) {
      this.loading = true;
      const { currentPassword, newPassword } = this.securityForm.value;

      // Aquí llamarías a tu servicio para cambiar la contraseña
      // Nota: Necesitas implementar changePassword en tu AuthService
      this.authService.changePassword(currentPassword, newPassword)
        .then(() => {
          toast.success('Contraseña actualizada correctamente');
          this.securityForm.reset();
          this.loading = false;
        })
        .catch((error) => {
          console.error(error);
          toast.error('Error: Verifica tu contraseña actual');
          this.loading = false;
        });
    } else {
      this.securityForm.markAllAsTouched();
    }
  }

  // Función auxiliar para actualizar la vista de la cabecera
  private updateHeaderInfo(fullName: string, email: string) {
    const nameToDisplay = fullName || 'Usuario';
    this.headerInfo = {
      name: nameToDisplay,
      email: email,
      // Toma la primera letra del nombre o del email para el avatar
      initial: nameToDisplay.charAt(0).toUpperCase()
    };
  }
}
