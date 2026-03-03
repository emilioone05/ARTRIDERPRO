export interface ReservationItem {
  id: number;
  title: string;
  price_per_day: number;
  image?: string;
  assigned_unit?: number;
  quantity?: number;
}

export interface ClientSummary {
  id: number;
  full_name: string;
  email: string;
  phone_number?: string;
}
//Esctructura
export interface ProviderReservation {
  id: number;
  reservation_code: string;
  start_date: string;
  end_date: string;
  status: string;
  total_price: number;

  // Datos del Proveedor
  client?: ClientSummary;
  items: ReservationItem[];
  days_count?: number;

  // CORRECCIÓN 2: Agregamos los campos del MODO CLIENTE como opcionales (?)
  // Así TypeScript no se queja cuando Angular intente leerlos en el HTML
  first_item_name?: string;
  first_item_image?: string;
  item_count?: number;
}
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[]; // Aquí es donde vendrá tu array de reservas
}
