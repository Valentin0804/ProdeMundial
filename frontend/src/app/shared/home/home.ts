import { Component, OnInit, NgZone, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { forkJoin } from 'rxjs';
import { GrupoService } from '../../core/services/grupo';
import { FixtureService } from '../../core/services/fixture';

@Component({
    selector: 'app-home',
    templateUrl: './home.html',
    styleUrls: ['./home.scss'],
    standalone: true,
    imports: [CommonModule, RouterModule]
})
export class HomeComponent implements OnInit {
    misGrupos: any[] = [];
    proximosPartidos: any[] = [];
    cargando = true;

    constructor(
        private grupoService: GrupoService,
        private fixtureService: FixtureService,
        private zone: NgZone,
        private cdr: ChangeDetectorRef
    ) { }


    copiarCodigo(codigo: string): void {
        navigator.clipboard.writeText(codigo);
        alert('¡Código copiado! Pasalo por WhatsApp a tus amigos.');
    }


    // home.ts
    ngOnInit(): void {
        this.cargando = true;

        // Usamos forkJoin para que todo aparezca de golpe y no por partes
        forkJoin({
            grupos: this.grupoService.getMisGrupos(),
            fixture: this.fixtureService.getFixtureGrupos()
        }).subscribe({
            next: (res: any) => {
                this.zone.run(() => {
                    // Procesar Grupos
                    const dataG = res.grupos.results || res.grupos;
                    this.misGrupos = Array.isArray(dataG) ? dataG : [];

                    // Procesar Partidos
                    this.proximosPartidos = this.extraerProximos(res.fixture);

                    this.cargando = false;

                    // Forzamos la detección inmediatamente después de asignar todo
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

            // Recorremos los grupos (A, B, C...)
            Object.values(data).forEach((grupo: any) => {
                // Recorremos las jornadas (Jornada 1, 2...)
                Object.values(grupo).forEach((jornada: any) => {
                    if (Array.isArray(jornada)) {
                        todosLosPartidos.push(...jornada);
                    }
                });
            });

            // Ordenar por fecha para mostrar los 3 que realmente siguen
            return todosLosPartidos
                .sort((a, b) => new Date(a.fecha_hora).getTime() - new Date(b.fecha_hora).getTime())
                .slice(0, 3);
        } catch (e) {
            console.error("Error procesando fixture para próximos partidos", e);
            return [];
        }
    }
}