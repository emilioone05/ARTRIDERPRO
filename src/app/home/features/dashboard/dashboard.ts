import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Category {
  id: string;
  name: string;
  imageUrl: string;
}

interface Equipment {
  id: number;
  title: string;
  providerName: string;
  pricePerDay: number;
  rating: number;
  reviewCount: number;
  imageUrl: string;
  isLiked: boolean;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrls: ['./dashboard.css']
})
export default class Dashboard {

  categories: Category[] = [
    { id: 'audio', name: 'Sonido', imageUrl: 'icons/sonido.png' },
    { id: 'lighting', name: 'Iluminación', imageUrl: 'icons/iluminacion.png' },
    { id: 'video', name: 'Video', imageUrl: 'icons/video.png' },
    { id: 'effects', name: 'Efectos', imageUrl: 'icons/efectos.png' },
  ];

  featuredEquipments: Equipment[] = [
    {
      id: 1,
      title: 'RCF ',
      providerName: 'Arnaut',
      pricePerDay: 90,
      rating: 4.8,
      reviewCount: 121,
      imageUrl: 'icons/sonido.png',
      isLiked: true
    },
    {
      id: 2,
      title: ' Consola',
      providerName: 'Dario cobos',
      pricePerDay: 25,
      rating: 4.9,
      reviewCount: 84,
      imageUrl: '',
      isLiked: false
    },
    {
      id: 3,
      title: 'Panel Led 3x3 Outdoor',
      providerName: 'Sound Pro',
      pricePerDay: 350,
      rating: 5.0,
      reviewCount: 15,
      imageUrl: '',
      isLiked: false
    },
    {
      id: 4,
      title: 'RCF',
      providerName: 'Andres Quesada',
      pricePerDay: 60,
      rating: 4.7,
      reviewCount: 42,
      imageUrl: '',
      isLiked: false
    },
    {
      id: 5,
      title: 'American Xtream CO2',
      providerName: 'Lona Music',
      pricePerDay: 95,
      rating: 4.9,
      reviewCount: 200,
      imageUrl: '',
      isLiked: false
    },
    {
      id: 6,
      title: 'L-Acoustics KS28 dual 18"',
      providerName: 'Acoustic Ecuador',
      pricePerDay: 135,
      rating: 4.9,
      reviewCount: 154,
      imageUrl: '',
      isLiked: false
    },
  ];
}
