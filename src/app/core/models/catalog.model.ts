export interface Publication {
  id: number;
  title: string;
  image: string;
  price_per_day: string;
  stock_count: string;
}

export interface SelectedItem {
  publication: Publication;
  quantity: number;
}
