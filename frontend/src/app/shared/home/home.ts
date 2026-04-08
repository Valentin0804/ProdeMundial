import { Component, OnInit, NgZone, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { DetalleGrupoComponent } from '../../grupos/detalle-grupo/detalle-grupo';
import { GrupoService } from '../../core/services/grupo';
import { FixtureService } from '../../core/services/fixture';

@Component({
    selector: 'app-home',
    templateUrl: './home.html',
    styleUrls: ['./home.scss'],
    standalone: true,
    imports: [CommonModule, RouterModule, DetalleGrupoComponent]
})
export class HomeComponent implements OnInit {
    misGrupos: any[] = [];
    grupoSeleccionadoId: number | null = null;
    proximosPartidos: any[] = [];
    cargando = true;

    constructor(
        private grupoService: GrupoService,
        private fixtureService: FixtureService,
        private zone: NgZone,
        private cdr: ChangeDetectorRef
    ) { }

    abrirDetalleGrupo(id: number) {
        this.grupoSeleccionadoId = id;
    }

    copiarCodigo(codigo: string): void {
        navigator.clipboard.writeText(codigo);
        alert('¡Código copiado! Pasalo por WhatsApp a tus amigos.');
    }

    ngOnInit(): void {
        this.cargando = true;

        forkJoin({
            grupos: this.grupoService.getMisGrupos(),
            fixture: this.fixtureService.getFixtureGrupos()
        }).subscribe({
            next: (res: any) => {
                this.zone.run(() => {
                    const dataG = res.grupos.results || res.grupos;
                    this.misGrupos = Array.isArray(dataG) ? dataG : [];

                    this.proximosPartidos = this.extraerProximos(res.fixture);

                    this.cargando = false;

                    this.cdr.detectChanges();
                });
            },
            error: () => {
                this.zone.run(() => {
                    this.cargando = false;
                    this.cdr.detectChanges();
                });
            }
        });
    }

    private extraerProximos(fixture: any): any[] {
        const data = fixture?.results || fixture;
        if (!data || typeof data !== 'object') return [];

        try {
            const todosLosPartidos: any[] = [];

            Object.values(data).forEach((grupo: any) => {
                Object.values(grupo).forEach((jornada: any) => {
                    if (Array.isArray(jornada)) {
                        todosLosPartidos.push(...jornada);
                    }
                });
            });

            return todosLosPartidos
                .sort((a, b) => new Date(a.fecha_hora).getTime() - new Date(b.fecha_hora).getTime())
                .slice(0, 3);
        } catch (e) {
            console.error("Error procesando fixture para próximos partidos", e);
            return [];
        }
    }
}