import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CrearGrupoComponent } from './crear-grupo/crear-grupo';
import { GruposRoutingModule } from './grupos-routing-module';

@NgModule({
    declarations: [
        CrearGrupoComponent // Declaramos el componente aquí
    ],
    imports: [
        CommonModule,
        FormsModule,    // IMPORTANTE: Para que funcione el [(ngModel)]
        RouterModule,
        GruposRoutingModule
    ]
})
export class GruposModule { }