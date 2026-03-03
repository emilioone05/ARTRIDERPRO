import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ProviderService } from '../../../../core/services/provider.service';

@Component({
  selector: 'app-publish-equipment',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './publish-equipment.html',
})
export class PublishEquipmentComponent implements OnInit {

  private router = inject(Router);
  private fb = inject(FormBuilder);
  private providerService = inject(ProviderService);
  private location = inject(Location);

  publishForm: FormGroup;
  isLoading = signal<boolean>(false);

  // Para la previsualización de la imagen
  currentImageUrl = signal<string | null>(null);
  selectedFile: File | null = null;
  categories = signal<any[]>([]);

  constructor() {
    this.publishForm = this.fb.group({
      title: ['', Validators.required],
      category: ['', Validators.required], // IMPORTANTE: En el HTML, el <select> debe guardar el ID, no el nombre.
      brand: ['', Validators.required],
      model: ['', Validators.required],
      description: ['', Validators.required],
      price_per_day: [null, [Validators.required, Validators.min(0)]],
      stock: [1, [Validators.required, Validators.min(1)]] // Usamos 'stock', tal cual.
    });
  }

  loadCategories() {
    this.providerService.getCategories().subscribe({
      next: (data: any) => {
        // Ajusta esto según si tu API devuelve un array directo o un objeto con results
        const listaCategorias = data.results ? data.results : data;
        this.categories.set(listaCategorias);
      },
      error: (err) => {
        console.error('Error conectando con API Categories:', err);
      }
    });
  }

  ngOnInit() {
    this.loadCategories();
  }

  // Detectar selección de archivo
  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedFile = file;
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
    // Verificamos si el formulario es válido y si hay imagen seleccionada
    if (this.publishForm.valid && this.selectedFile) {
      this.isLoading.set(true);

      const formData = new FormData();

      // Obtenemos los valores limpios del formulario
      const formValues = this.publishForm.value;

      // --- ASIGNACIÓN MANUAL (Más segura que el bucle) ---

      // 1. Datos básicos
      formData.append('title', formValues.title);
      formData.append('description', formValues.description);
      formData.append('price_per_day', formValues.price_per_day);

      // 2. Datos para crear el Producto (Brand, Model, Category)
      // El backend interceptará esto para crear el CatalogProduct
      formData.append('brand', formValues.brand);
      formData.append('model', formValues.model);
      formData.append('category', formValues.category); // Asegúrate que esto sea el ID (número)

      // 3. Stock
      // Enviamos 'stock' directo. El Serializer corregido se encargará de crear las Units.
      formData.append('stock', formValues.stock);

      // 4. Depósito de garantía (Calculado automáticamente)
      const price = formValues.price_per_day || 0;
      formData.append('guarantee_amount', (price * 0.5).toString());

      // 5. La Imagen
      formData.append('image', this.selectedFile);

      // --- ENVIAR AL SERVICIO ---
      this.providerService.createPublication(formData).subscribe({
        next: () => {
          alert('¡Equipo publicado con éxito!');
          this.router.navigate(['/provider/catalog']);
        },
        error: (err) => {
          console.error('Error publicando', err);
          // Esto te mostrará en consola exactamente qué campo rechaza el backend si falla
          if (err.error) console.log('Detalle del error Backend:', err.error);
          this.isLoading.set(false);
        }
      });
    } else {
      // Opcional: Avisar al usuario si falta algo (como la imagen)
      alert('Por favor completa el formulario y selecciona una imagen.');
    }
  }
}
