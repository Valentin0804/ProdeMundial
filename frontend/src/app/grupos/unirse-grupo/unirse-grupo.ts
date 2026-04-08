import { Component } from '@angular/core';
import { GrupoService } from '../../core/services/grupo';
import { Router } from '@angular/router';

@Component({
    selector: 'app-unirse-grupo',
    standalone: false,
    templateUrl: './unirse-grupo.html',
    styleUrls: ['./unirse-grupo.scss']
})
export class UnirseGrupoComponent {
    codigoInvitacion = '';
    cargando = false;
    error = '';
    mensajeExito = '';

    constructor(
        private grupoService: GrupoService,
        private router: Router
    ) { }

    unirse() {
        if (!this.codigoInvitacion) return;

        this.cargando = true;
        this.error = '';
        this.mensajeExito = '';

        const codigo = this.codigoInvitacion.trim().toUpperCase();

        this.grupoService.unirseAGrupo(codigo).subscribe({
            next: (res) => {
                this.mensajeExito = `¡Te uniste correctamente a ${res.nombre}!`;
                this.cargando = false;
                setTimeout(() => this.router.navigate(['/home']), 1500);

            },
            error: (err) => {
                this.cargando = false;
                this.error = err.error?.error || 'Error al unirse al grupo.';
                console.error('Detalle del error:', err);
            }
        });
    }
}