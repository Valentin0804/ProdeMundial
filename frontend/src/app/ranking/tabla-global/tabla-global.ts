import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PronosticoService } from '../../core/services/pronostico';

@Component({
  selector: 'app-tabla-global',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tabla-global.html',
  styleUrl: './tabla-global.scss',
})
export class TablaGlobal implements OnInit {
  rankingCompleto: any[] = []; // Los 100 que vienen del back
  rankingFiltrado: any[] = []; // Lo que se muestra según el botón (5, 10, etc)
  miPosicion: any = null;
  filtroActual = 100;
  torneoEmpezado = false;
  cargando = true;
  error: string | null = null;


  constructor(private pronosticoService: PronosticoService, private cdr: ChangeDetectorRef) { }

  ngOnInit(): void {
    this.cargarRanking();
  }

  cargarRanking(): void {
    this.pronosticoService.getRankingGlobal().subscribe({
      next: (res: any) => {
        console.log('Datos recibidos del back:', res);
        // Asumiendo que el back devuelve { top_100: [...], mi_posicion: {...} }
        this.rankingCompleto = res.top_100 || [];
        this.miPosicion = res.mi_posicion;
        this.aplicarFiltro(100);
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'No se pudo cargar el ranking global.';
        this.cargando = false;
      },
    });
  }

  aplicarFiltro(cantidad: number): void {
    this.filtroActual = cantidad;
    this.rankingFiltrado = this.rankingCompleto.slice(0, cantidad);
  }

  estaEnTablaVisible(): boolean {
    if (!this.miPosicion || !this.rankingFiltrado.length) return false;
    // Si mi posición es menor o igual a la cantidad filtrada, ya estoy en la lista
    return this.miPosicion.posicion <= this.filtroActual;
  }
}