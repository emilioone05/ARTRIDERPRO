import { CatalogComponent } from '../../provider/features/catalog/catalog';
export interface CatalogStats {
  totalItems: number;
  totalStock: number;
  totalPackages: number;
}

export interface CatalogItem {
  id: number;
  title: string;
  // name: string;
  description: string;
  pricePerDay: number;
  image?: string;
  stock: number;
  type: 'equipo' | 'paquete';
  category: string;
}

export interface CatalogResponse {
  stats: CatalogStats;
  items: CatalogItem[];
}
