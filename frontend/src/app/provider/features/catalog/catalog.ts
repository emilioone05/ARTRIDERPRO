import { Component, signal, computed, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProviderService } from '../../../core/services/provider.service';
import { CatalogItem, CatalogStats } from '../../../core/interfaces/provider-dashboard.interface';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-catalog',
  standalone: true,
  imports: [CommonModule,FormsModule,RouterLink],
  templateUrl: './catalog.html',
})
export class CatalogComponent implements OnInit {

  private providerService = inject(ProviderService);
  private baseUrl = 'http://127.0.0.1:8000';
  activeTab = signal<'equipo' | 'paquete'>('equipo');
  isLoading = signal<boolean>(true);

  searchQuery = signal<string>(''); // <--- Señal para el buscador
  // Estadísticas
  stats = signal<CatalogStats>({
    totalItems: 0,
    totalStock: 0,
    totalPackages: 0
  });

  items = signal<CatalogItem[]>([]);

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.isLoading.set(true);

    this.providerService.getCatalogData().subscribe({
      next: (data) => {
        console.log('Datos recibidos de Django (Catálogo):', data);
        this.stats.set(data.stats);
        this.items.set(data.items);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error conectando con Django:', err);
        this.isLoading.set(false);
      }
    });
  }

  filteredItems = computed(() => {
    const currentTab = this.activeTab();
    const query = this.searchQuery().toLowerCase();

    return this.items().filter(item => {
      const matchesTab = item.type === currentTab;
      const matchesSearch = item.title.toLowerCase().includes(query) ||
                            item.description.toLowerCase().includes(query);
      return matchesTab && matchesSearch;
    });
  });
  countEquipos = computed(() => this.items().filter(i => i.type === 'equipo').length);
  countPaquetes = computed(() => this.items().filter(i => i.type === 'paquete').length);
  switchTab(tab: 'equipo' | 'paquete') {
    this.activeTab.set(tab);
  }
  getFullImageUrl(imagePath: string | null | undefined): string {
    if (!imagePath) {
      return 'assets/placeholder.jpg'; // Retorna placeholder si es null
    }

    // Si la imagen ya viene con http (ej: bucket de Amazon S3), la devolvemos tal cual
    if (imagePath.startsWith('http')) {
      return imagePath;
    }

    // Si no, le pegamos el dominio de Django al principio
    return `${this.baseUrl}${imagePath}`;
  }

}
