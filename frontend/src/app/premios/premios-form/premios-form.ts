import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PremioService } from '../../core/services/premio';

@Component({
  selector: 'app-premios-form',
  templateUrl: './premios-form.html',
  styleUrls: ['./premios-form.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule]
})

export class PremiosForm implements OnInit {
  pronostico: any = {};
  candidatos: any = {};
  buscandoEn: string | null = null;
  candidatosFiltrados: any[] = [];
  estaBloqueado: boolean = false;
  mostrarModalConfirmar: boolean = false;
  guardando: boolean = false;

  categorias = [
    { key: 'bota_de_oro', titulo: 'Bota de Oro', puntos: 4 },
    { key: 'balon_de_oro', titulo: 'Balón de Oro', puntos: 4 },
    { key: 'guante_de_oro', titulo: 'Guante de Oro', puntos: 4 },
    { key: 'mejor_joven', titulo: 'Mejor Joven', puntos: 4 },
  ];

  codigosPaises: { [key: string]: string } = {
    'ARG': 'ar',
    'ESP': 'es',
    'POR': 'pt',
    'FRA': 'fr',
    'BRA': 'br',
    'ENG': 'gb-eng',
    'GER': 'de',
    'URU': 'uy',
    'COL': 'co',
    'BEL': 'be',
    'NOR': 'no',
    'CRO': 'hr',
    'ITA': 'it',
    'NED': 'nl',
    'TUR': 'tr',
  };

  constructor(private premioService: PremioService, private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.premioService.getCandidatos().subscribe({
      next: (res) => {
        this.candidatos = res;
        this.obtenerEstadoActual();
      }
    });
  }

  cargarDatos() {
    this.premioService.getCandidatos().subscribe({
      next: (res) => {
        this.candidatos = res;
        this.obtenerEstadoActual();
      }
    });
  }

  obtenerEstadoActual() {
    this.premioService.getPronosticoUsuario().subscribe({
      next: (data) => {
        console.log("Datos del servidor:", data); // REVISA ESTO EN CONSOLA
        if (data) {
          this.pronostico = data;

          // Reconstrucción de detalles
          this.categorias.forEach(cat => {
            // Buscamos el ID. Ojo: verifica si el back devuelve 'bota_de_oro' o 'bota_de_oro_id'
            const jugadorId = this.pronostico[cat.key];
            if (jugadorId) {
              const lista = this.candidatos[cat.key] || [];
              const detalle = lista.find((p: any) => p.id === jugadorId);
              if (detalle) {
                this.pronostico[cat.key + '_detalle'] = detalle;
              }
            }
          });

          // Cambiamos la lógica de bloqueo:
          // Si el servidor dice que ya está bloqueado por tiempo O si ya hay datos guardados
          if (data.bloqueado) {
            this.estaBloqueado = true;
          } else {
            // Si no está bloqueado por tiempo, vemos si ya completó el pronóstico
            this.verificarBloqueo();
          }

          this.cdr.detectChanges();
        }
      }
    });
  }

  verificarBloqueo() {
    const keys = this.categorias.map(c => c.key);
    // Si TODOS los campos tienen un valor (ID de jugador), bloqueamos la edición
    this.estaBloqueado = keys.every(key =>
      this.pronostico[key] !== null && this.pronostico[key] !== undefined
    );
  }

  abrirBuscador(key: string) {
    if (this.estaBloqueado) {
      alert("Tus premios ya están guardados y no se pueden modificar.");
      return;
    }
    this.buscandoEn = key;
    this.candidatosFiltrados = this.candidatos[key] || [];
  }

  filtrar(event: any) {
    const term = event.target.value.toLowerCase().trim();
    const key = this.buscandoEn;

    if (!key || !this.candidatos[key]) {
      this.candidatosFiltrados = [];
      return;
    }

    if (!term) {
      this.candidatosFiltrados = [...this.candidatos[key]];
      return;
    }

    this.candidatosFiltrados = this.candidatos[key].filter((p: any) => {
      const nombre = p.nombre ? p.nombre.toLowerCase() : '';
      const apellido = p.apellido ? p.apellido.toLowerCase() : '';
      return nombre.includes(term) || apellido.includes(term);
    });
  }

  seleccionar(jugador: any) {
    if (!this.buscandoEn || this.estaBloqueado) return;

    const key = this.buscandoEn;
    this.pronostico[key] = jugador.id;
    this.pronostico[key + '_detalle'] = jugador;

    this.buscandoEn = null;
    this.candidatosFiltrados = [];

    this.cdr.detectChanges();
  }

  confirmarEnvio() {
    // Validación previa: Asegurarse de que eligió los 4 antes de enviar
    const keys = this.categorias.map(c => c.key);
    const incompleto = keys.some(key => !this.pronostico[key]);

    if (incompleto) {
      alert("Por favor, selecciona un candidato para todas las categorías.");
      this.mostrarModalConfirmar = false;
      this.guardando = false;
      return;
    }

    this.guardando = true;

    const datosParaEnviar = {
      bota_de_oro: this.pronostico.bota_de_oro,
      balon_de_oro: this.pronostico.balon_de_oro,
      guante_de_oro: this.pronostico.guante_de_oro,
      mejor_joven: this.pronostico.mejor_joven
    };

    this.premioService.guardarPronostico(datosParaEnviar).subscribe({
      next: () => {
        // SOLUCIÓN 2: Forzamos el estado de bloqueo tras el éxito
        this.estaBloqueado = true;
        this.mostrarModalConfirmar = false;
        this.guardando = false;
        alert("¡Pronóstico guardado con éxito!");
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.guardando = false;
        console.error("Detalle del error 400:", err.error); // <--- ESTO te dirá la verdad
        alert("Error: " + JSON.stringify(err.error)); // Para verlo en el celular/alerta
      }
    });
  }

  getBandera(codigoOriginal: string) {
    if (!codigoOriginal) return '';
    const cod = codigoOriginal.trim().toUpperCase();
    const codigo2Letras = this.codigosPaises[cod] || cod.substring(0, 2).toLowerCase();

    return `https://flagcdn.com/w40/${codigo2Letras}.png`;
  }


}