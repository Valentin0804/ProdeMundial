import { Component, Input, Output, EventEmitter, OnInit, ChangeDetectorRef } from '@angular/core';
import { GrupoService } from '../../core/services/grupo';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-detalle-grupo',
    standalone: true,
    templateUrl: './detalle-grupo.html',
    styleUrls: ['./detalle-grupo.scss'],
    imports: [CommonModule]
})

export class DetalleGrupoComponent implements OnInit {
    @Input() grupoId!: number;
    @Output() onCerrar = new EventEmitter<void>();

    infoGrupo: any = null;
    cargando = true;
    idLogueado: number = 0;

    constructor(
        private grupoService: GrupoService,
        private router: Router,
        private cdr: ChangeDetectorRef
    ) { }

    ngOnInit() {
        this.grupoService.getDetalleModal(this.grupoId).subscribe({
            next: (data) => {
                this.infoGrupo = data;
                this.cargando = false;
                this.cdr.detectChanges();
            },
            error: (err) => {
                console.error("Error al cargar:", err);
                this.cargando = false;
                this.cdr.detectChanges()
            }
        });
    }

    cargarDatos() {
        this.cargando = true;
        this.grupoService.getDetalleModal(this.grupoId).subscribe({
            next: (res) => {
                this.infoGrupo = res;
                this.cargando = false;
            },
            error: () => this.cerrar()
        });
    }

    eliminarMiembro(usuarioId: number) {
        if (confirm('¿Eliminar a este usuario del grupo?')) {
            this.grupoService.eliminarMiembro(this.grupoId, usuarioId).subscribe(() => {
                this.cargarDatos();
            });
        }
    }

    salirDelGrupo() {
        if (confirm('¿Estás seguro de que quieres salir del grupo?')) {
            this.grupoService.salirDelGrupo(this.grupoId).subscribe(() => {
                this.cerrar();
                location.reload();
            });
        }
    }

    verPredicciones(usuarioId: number) {
        this.cerrar();
        this.router.navigate(['/pronosticos/ver', usuarioId]);
    }

    cerrar() {
        this.onCerrar.emit();
    }
}