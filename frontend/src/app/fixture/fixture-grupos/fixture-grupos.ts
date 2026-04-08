import { Component, OnInit, NgZone, ChangeDetectorRef } from '@angular/core';
import { FixtureService, FixtureGrupos, Partido } from '../../core/services/fixture';
import { PronosticoService, Pronostico } from '../../core/services/pronostico';
import { forkJoin, Observable } from 'rxjs';

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
  fase = 'grupos';
  eliminatoriasHabilitadas = false;
  pronosticos = new Map<number, Pronostico>();
  inputValues = new Map<number, { local: number | null, visitante: number | null }>();
  gruposCompletados = new Set<string>();
  guardandoBackend = false;
  cargando = true;
  error = '';

  constructor(
    private fixtureService: FixtureService,
    private pronosticoService: PronosticoService,
    private zone: NgZone,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargando = true;
    forkJoin({
      fixture: this.fixtureService.getFixtureGrupos(),
      misPronosticos: this.pronosticoService.getMisPronosticos()
    }).subscribe({
      next: (res: any) => {
        this.fixture = res.fixture.results || res.fixture;
        this.grupos = Object.keys(this.fixture).sort();

        const lista = res.misPronosticos.results || res.misPronosticos;
        if (Array.isArray(lista)) {
          lista.forEach(p => {
            this.pronosticos.set(p.partido, p);
            this.inputValues.set(p.partido, { local: p.goles_local, visitante: p.goles_visitante });
          });
        }

        this.actualizarEstadosDeGrupos();
        this.cargando = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.error = 'Error al cargar los datos.';
        this.cargando = false;
      }
    });
  }

  cambiarFase(fase: string): void {
    if (fase === 'eliminatorias' && !this.eliminatoriasHabilitadas) return;
    this.fase = fase;
  }

  cambiarFaseGrupo(grupo: string): void {
    this.grupoActivo = grupo;
  }

  grupoCompletado(grupo: string): boolean {
    return this.gruposCompletados.has(grupo);
  }

  validarGrupoCompleto(grupo: string): boolean {
    let completo = true;
    const jornadas = this.getJornadas(grupo);
    if (jornadas.length === 0) return false;

    jornadas.forEach(j => {
      this.getPartidos(grupo, j).forEach(p => {
        const val = this.inputValues.get(p.id);
        if (!val || val.local === null || val.visitante === null) {
          completo = false;
        }
      });
    });
    return completo;
  }

  setInput(partidoId: number, equipo: 'local' | 'visitante', valor: string): void {
    if (this.grupoCompletado(this.grupoActivo)) return;

    const v = valor === '' ? null : parseInt(valor);
    const actual = this.inputValues.get(partidoId) || { local: null, visitante: null };

    if (equipo === 'local') actual.local = v;
    else actual.visitante = v;

    this.inputValues.set(partidoId, { ...actual });
  }

  getInput(partidoId: number, equipo: 'local' | 'visitante'): number | null {
    const val = this.inputValues.get(partidoId);
    return val ? (equipo === 'local' ? val.local : val.visitante) : null;
  }

  guardarGrupoEnBaseDeDatos(grupo: string): void {
    if (!this.validarGrupoCompleto(grupo)) return;

    this.guardandoBackend = true;
    const peticiones: Observable<Pronostico>[] = [];

    this.getJornadas(grupo).forEach(j => {
      this.getPartidos(grupo, j).forEach(p => {
        const val = this.inputValues.get(p.id);
        if (val) {
          peticiones.push(this.pronosticoService.guardarOActualizar(this.pronosticos, p.id, val.local!, val.visitante!));
        }
      });
    });

    forkJoin(peticiones).subscribe({
      next: (resultados) => {
        resultados.forEach((p: any) => this.pronosticos.set(p.partido, p));
        this.gruposCompletados.add(grupo);
        this.guardandoBackend = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.guardandoBackend = false;
        alert('Hubo un error al guardar el grupo.');
      }
    });
  }

  actualizarEstadosDeGrupos(): void {
    this.grupos.forEach(g => {
      const pTotal = this.progreso(g);
      if (pTotal.cargados === pTotal.total && pTotal.total > 0) {
        this.gruposCompletados.add(g);
      }
    });
  }

  getJornadas(grupo: string): string[] { return Object.keys(this.fixture[grupo] || {}).sort(); }

  getPartidos(grupo: string, jornada: string): Partido[] { return this.fixture[grupo]?.[jornada] || []; }

  getPuntos(partidoId: number): number | null { return this.pronosticos.get(partidoId)?.puntos_obtenidos ?? null; }

  progreso(grupo: string): { total: number, cargados: number } {
    let total = 0, cargados = 0;
    this.getJornadas(grupo).forEach(j => {
      this.getPartidos(grupo, j).forEach(p => {
        total++;
        if (this.pronosticos.has(p.id)) cargados++;
      });
    });
    return { total, cargados };
  }
}