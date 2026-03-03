import { Component, inject, OnInit, signal } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ProviderService } from '../../../../core/services/provider.service';
// Aseguate de que la ruta al service sea correcta

@Component({
  selector: 'app-edit-equipment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './edit-equipment.html',
})
export class EditEquipmentComponent implements OnInit {

  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private fb = inject(FormBuilder);
  private providerService = inject(ProviderService);
  private location = inject(Location);

  editForm: FormGroup;
  equipmentId = signal<number | null>(null);
  isLoading = signal<boolean>(true);

  // Para previsualizar la imagen
  currentImageUrl = signal<string | null>(null);
  selectedFile: File | null = null;

  // Opciones para el Select
  categories = ['Sonido', 'Iluminación', 'Pantallas', 'Estructuras', 'DJ Booth'];

  constructor() {
    this.editForm = this.fb.group({
      title: ['', Validators.required],
      category: ['', Validators.required],
      description: ['', Validators.required],
      price_per_day: [0, [Validators.required, Validators.min(0)]],
      stock: [1, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    // 1. Obtener el ID de la URL
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.equipmentId.set(+id);
      this.loadEquipmentData(+id);
    }
  }

  loadEquipmentData(id: number) {
    console.log('1. Buscando ID:', id); // ¿El ID es correcto?

    this.providerService.getPublicationById(id).subscribe({
      next: (data) => {
        console.log('2. Datos recibidos de Django:', data); // ¡AQUÍ ESTÁ LA CLAVE!

        // Vamos a ver si el mapeo funciona antes de aplicarlo
        const patchData = {
          title: data.title,
          description: data.description,
          price_per_day: data.price_per_day,
          stock: data.stock_count || 1, // A veces viene como stock_count
          // OJO AQUÍ: Revisa en la consola cómo se llama exactamente este campo en tu JSON
          category: data.product_details?.category_name || data.category || 'General'
        };

        console.log('3. Datos que voy a poner en el form:', patchData);

        this.editForm.patchValue(patchData);

        // Forzar actualización de la imagen
        if (data.image) {
            // Asegúrate de que venga con http, si no, concáténalo
            const imgUrl = data.image.startsWith('http') ? data.image : `http://127.0.0.1:8000${data.image}`;
            this.currentImageUrl.set(imgUrl);
        }

        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error cargando:', err);
        this.isLoading.set(false);
      }
    });
  }
  // Detectar cambio de archivo (Nueva foto)
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;

      // Crear preview instantáneo
      const reader = new FileReader();
      reader.onload = () => {
        this.currentImageUrl.set(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  }

  goBack() {
    this.location.back();
  }

  onSubmit() {
    if (this.editForm.valid && this.equipmentId()) {
      this.isLoading.set(true);

      const formData = new FormData();
      // Agregamos textos
      Object.keys(this.editForm.controls).forEach(key => {
        formData.append(key, this.editForm.get(key)?.value);
      });

      // Agregamos imagen SOLO si cambió
      if (this.selectedFile) {
        formData.append('image', this.selectedFile);
      }

      this.providerService.updatePublication(this.equipmentId()!, formData).subscribe({
        next: () => {
          // Éxito: volvemos al catálogo
          this.router.navigate(['/provider/catalog']);
        },
        error: (err) => {
          console.error('Error actualizando', err);
          alert('Error al guardar cambios');
          this.isLoading.set(false);
        }
      });
    }
  }
}
