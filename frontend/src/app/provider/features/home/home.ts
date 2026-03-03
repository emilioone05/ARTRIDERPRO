import { Component, inject, signal, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProviderService, ProviderHomeStats } from '../../../core/services/provider.service';

@Component({
  selector: 'app-provider-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.html',
})
export class HomeComponent implements OnInit {
  private providerService = inject(ProviderService);

  isLoading = signal(true);

  stats = signal<ProviderHomeStats>({
    company_name: '',
    email: '',
    phone: '',
    location: '',
    published_equipments: 0,
    active_reservations: 0
  });

  ngOnInit() {
    this.providerService.getHomeStats().subscribe({
      next: (data) => {
        this.stats.set(data);
        this.isLoading.set(false);
      },
      error: (e) => {
        console.error(e);
        this.isLoading.set(false);
      }
    });
  }
}
