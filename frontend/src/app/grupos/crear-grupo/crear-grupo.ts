import { Component } from '@angular/core';
import { GrupoService } from '../../core/services/grupo';
import { Router } from '@angular/router';

@Component({
    selector: 'app-crear-grupo',
    standalone: false, // Recordá usar false ya que usamos módulos
    templateUrl: './crear-grupo.html',
    styleUrls: ['./crear-grupo.scss']
})
export class CrearGrupoComponent {
    nombreGrupo = '';
    cargando = false;
    error = '';

    constructor(private grupoService: GrupoService, private router: Router) { }

    crear() {
        if (!this.nombreGrupo) return;
        this.cargando = true;

        this.grupoService.crearGrupo(this.nombreGrupo).subscribe({
            next: (res) => {
                alert(`¡Grupo creado! Código: ${res.codigo_invitacion}`);
                this.router.navigate(['/fixture']); // O a donde quieras mandarlo
            },
            error: (err) => {
                this.error = 'Error al crear el grupo.';
                this.cargando = false;
            }
        });
    }
}