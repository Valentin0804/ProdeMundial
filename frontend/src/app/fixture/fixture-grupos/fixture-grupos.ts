import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FixtureService, FixtureGrupos, Partido } from '../../core/services/fixture';
import { PronosticoService, Pronostico } from '../../core/services/pronostico';

@Component({
  selector: 'app-fixture-grupos',
  standalone: false,
  templateUrl: './fixture-grupos.html',
  styleUrls: ['./fixture-grupos.scss']
})
export class FixtureGruposComponent implements OnInit {
  fixture: FixtureGrupos = {};
  grupos: string[] = [];
  grupoActivo = 'A';
  pronosticos = new Map<number, Pronostico>();
  // Valores temporales mientras el usuario escribe
  inputValues = new Map<number, { local: number | null, visitante: number | null }>();
  guardando = new Set<number>();
  cargando = true;
  error = '';

  constructor(
    private fixtureService: FixtureService,
    private pronosticoService: PronosticoService
  ) { }

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargando = false;
    this.fixtureService.getFixtureGrupos().subscribe({
      next: (data) => {
        this.fixture = data;
        this.grupos = Object.keys(data).sort();
        if (this.grupos.length) this.grupoActivo = this.grupos[0];
        this.cargarPronosticos();
      },
      error: () => {
        this.error = 'Error al cargar el fixture.';
        this.cargando = false;
      }
    });
  }

  cargarPronosticos(): void {
    this.pronosticoService.getMisPronosticos().subscribe({
      next: (data) => {
        data.forEach(p => this.pronosticos.set(p.partido, p));
        this.cargando = false;
      },
      error: () => { this.cargando = false; }
    });
  }

  getJornadas(grupo: string): string[] {
    return Object.keys(this.fixture[grupo] || {}).sort();
  }

  getPartidos(grupo: string, jornada: string): Partido[] {
    return this.fixture[grupo]?.[jornada] || [];
  }

  getInput(partidoId: number, equipo: 'local' | 'visitante'): number | null {
    const inp = this.inputValues.get(partidoId);
    if (inp) return equipo === 'local' ? inp.local : inp.visitante;
    const pro = this.pronosticos.get(partidoId);
    if (pro) return equipo === 'local' ? pro.goles_local : pro.goles_visitante;
    return null;
  }

  setInput(partidoId: number, equipo: 'local' | 'visitante', valor: string): void {
    const v = valor === '' ? null : parseInt(valor);
    const actual = this.inputValues.get(partidoId) || {
      local: this.getInput(partidoId, 'local'),
      visitante: this.getInput(partidoId, 'visitante')
    };
    if (equipo === 'local') actual.local = v;
    else actual.visitante = v;
    this.inputValues.set(partidoId, actual);
  }

  guardar(partido: Partido): void {
    if (partido.bloqueado) return;
    const inp = this.inputValues.get(partido.id);
    const gl = inp?.local ?? this.getInput(partido.id, 'local');
    const gv = inp?.visitante ?? this.getInput(partido.id, 'visitante');
    if (gl === null || gv === null) return;

    this.guardando.add(partido.id);
    this.pronosticoService.guardarOActualizar(this.pronosticos, partido.id, gl, gv).subscribe({
      next: (p) => {
        this.pronosticos.set(partido.id, p);
        this.inputValues.delete(partido.id);
        this.guardando.delete(partido.id);
      },
      error: () => this.guardando.delete(partido.id)
    });
  }

  getPuntos(partidoId: number): number | null {
    return this.pronosticos.get(partidoId)?.puntos_obtenidos ?? null;
  }

  tienePronostico(partidoId: number): boolean {
    return this.pronosticos.has(partidoId);
  }

  estaGuardando(partidoId: number): boolean {
    return this.guardando.has(partidoId);
  }

  progreso(grupo: string): { total: number, cargados: number } {
    let total = 0, cargados = 0;
    this.getJornadas(grupo).forEach(j => {
      this.getPartidos(grupo, j).forEach(p => {
        total++;
        if (this.tienePronostico(p.id)) cargados++;
      });
    });
    return { total, cargados };
  }
}