import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule,Location } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { ProviderService } from '../../../../core/services/provider.service';

interface SelectedItem {
  id: number;
  title: string;
  image: string;
  price: number;
  quantity: number;
}

@Component({
  selector: 'app-create-package',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule,RouterLink],
  templateUrl: './publish-package.html'
})
export class PublishPackageComponent implements OnInit {
  private location = inject(Location);
  private fb = inject(FormBuilder);
  private providerService = inject(ProviderService);
  private router = inject(Router);

  packageForm: FormGroup = this.fb.group({
    title: ['', Validators.required],
    description: ['', Validators.required],
    price: [0, [Validators.required, Validators.min(0)]],
    image: [null]
  });

  isModalOpen = signal<boolean>(false);
  isLoadingItems = signal<boolean>(false);

  availableEquipments = signal<any[]>([]);
  tempSelection = signal<Map<number, SelectedItem>>(new Map());

  // Lista FINAL de equipos agregados al formulario (Para mostrar en la "caja gris")
  addedItems = signal<SelectedItem[]>([]);

  ngOnInit() {
    this.loadMyEquipments();
  }

  // 1. Cargar equipos para el modal
  loadMyEquipments() {
    this.isLoadingItems.set(true);
    this.providerService.getMyPublications().subscribe({
      next: (resp: any) => {
        // Tu Swagger dice que viene en 'results'
        this.availableEquipments.set(resp.results || []);
        this.isLoadingItems.set(false);
      },
      error: (err) => {
        console.error('Error cargando equipos', err);
        this.isLoadingItems.set(false);
      }
    });
  }

  // --- LÓGICA DEL MODAL (Imagen 2) ---

  openModal() {
    this.isModalOpen.set(true);
    // Reiniciamos la selección temporal basada en lo que ya se agregó antes
    const currentMap = new Map<number, SelectedItem>();
    this.addedItems().forEach(item => currentMap.set(item.id, item));
    this.tempSelection.set(currentMap);
  }

  closeModal() {
    this.isModalOpen.set(false);
  }
  goBack() {
    this.location.back();
  }

  // Cuando marcas/desmarcas el checkbox
  toggleItemSelection(item: any, isChecked: boolean) {
    const currentMap = new Map(this.tempSelection());

    if (isChecked) {
      // Agregamos al mapa con cantidad 1 inicial
      currentMap.set(item.id, {
        id: item.id,
        title: item.title,
        image: item.image,
        price: parseFloat(item.price_per_day),
        quantity: 1
      });
    } else {
      currentMap.delete(item.id);
    }
    this.tempSelection.set(currentMap);
  }

  // Cuando cambias el numerito (input number) en el modal
  updateQuantity(id: number, qty: number) {
    const currentMap = new Map(this.tempSelection());
    const item = currentMap.get(id);
    if (item && qty > 0) {
      item.quantity = qty;
      currentMap.set(id, item);
      this.tempSelection.set(currentMap);
    }
  }

  // Helpers para el HTML del modal
  isItemSelected(id: number): boolean {
    return this.tempSelection().has(id);
  }

  getItemQuantity(id: number): number {
    return this.tempSelection().get(id)?.quantity || 1;
  }

  // Botón "Agregar seleccionados" del modal
  confirmAddItems() {
    // Convertimos el mapa a array y lo guardamos en la lista final
    const items = Array.from(this.tempSelection().values());
    this.addedItems.set(items);
    this.closeModal();
  }

  // Eliminar un item de la lista final (fuera del modal)
  removeItem(index: number) {
    const current = this.addedItems();
    current.splice(index, 1);
    this.addedItems.set([...current]);
  }

  // --- GUARDAR TODO ---
  onSubmit() {
    if (this.packageForm.invalid) {
      alert('Por favor completa los campos requeridos');
      return;
    }
    if (this.addedItems().length === 0) {
      alert('Debes agregar al menos un equipo al paquete');
      return;
    }

    // Preparamos el JSON para el Backend
    const payload = {
      title: this.packageForm.get('title')?.value,
      description: this.packageForm.get('description')?.value,
      price: this.packageForm.get('price')?.value,
      // Array de items con ID y Cantidad
      items: this.addedItems().map(item => ({
        publication_id: item.id,
        quantity: item.quantity
      }))
    };

    console.log('Enviando paquete:', payload);

    this.providerService.createPackage(payload).subscribe({
      next: () => {
        alert('Paquete creado con éxito');
        this.router.navigate(['/provider/catalog']); // Volver al catálogo
      },
      error: (err) => {
        console.error('Error creando paquete', err);
        alert('Hubo un error al crear el paquete');
      }
    });
  }
}
