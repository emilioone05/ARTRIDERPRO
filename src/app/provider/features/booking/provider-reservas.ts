import { Component, signal, inject, OnInit, effect } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { AuthStateService } from '../../../shared/data-acces/auth-state.service'; // Para saber el modo
import {BookingService} from '../../../core/services/bookin.service';
import { ProviderReservation ,PaginatedResponse} from '../../../core/models/reservation.model';
@Component({
  selector: 'app-provider-reservas',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './provider-reservas.html' // Lo pondremos en archivo separado para orden
})
export class ProviderReservationsComponent implements OnInit {

  private bookingService = inject(BookingService);
  private location = inject(Location);
  private router = inject(Router);

  reservations = signal<ProviderReservation[]>([]);
  isLoading = signal<boolean>(true);

  isProviderMode = signal<boolean>(false);

  constructor() {
    this.isProviderMode.set(this.router.url.includes('/provider'));
  }

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.isLoading.set(true);

    // Tipamos la respuesta esperada
    this.bookingService.getReservations(this.isProviderMode())
      .subscribe({
        next: (data: PaginatedResponse<ProviderReservation>) => {
          // Si tu backend devuelve { count: 1, results: [...] }
          if (data.results) {
             this.reservations.set(data.results);
          } else {
             // Por si acaso devolviera el array directo (defensivo)
             this.reservations.set(data as any);
          }
          this.isLoading.set(false);
        },
        error: (err) => {
          console.error('Error cargando reservas', err);
          this.isLoading.set(false);
        }
      });
  }
  private updateStatus(id: number, newStatus: string) {
    this.isLoading.set(true);
    // Necesitas agregar este método 'updateReservationStatus' en tu BookingService
    this.bookingService.updateReservationStatus(id, newStatus).subscribe({
      next: () => {
        // Actualización Optimista: Actualizamos la lista local sin recargar todo
        this.reservations.update(current =>
          current.map(res =>
            res.id === id ? { ...res, status: newStatus } : res
          )
        );
        this.isLoading.set(false);
        alert(`Reserva ${newStatus.toLowerCase()} con éxito.`);
      },
      error: (err) => {
        console.error('Error al actualizar', err);
        this.isLoading.set(false);
        alert('Hubo un error al actualizar el estado.');
      }
    });
  }

  goBack() {
    this.location.back();
  }

  // Helpers para colores de estado
  getStatusClass(status: string): string {
    switch (status) {
      case 'CONFIRMADA': return 'bg-green-100 text-green-800';
      case 'PENDIENTE': return 'bg-yellow-100 text-yellow-800';
      case 'FINALIZADA': return 'bg-blue-100 text-blue-800';
      case 'CANCELADA': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }
  approveReservation(id: number) {
    if(!confirm('¿Estás seguro de aprobar esta reserva?')) return;
    this.updateStatus(id, 'CONFIRMADA');
  }

  rejectReservation(id: number) {
    if(!confirm('¿Quieres rechazar esta reserva?')) return;
    this.updateStatus(id, 'CANCELADA'); // O 'RECHAZADA' según tu backend
  }

}
