import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CrearGrupoComponent } from './crear-grupo/crear-grupo';
import { UnirseGrupoComponent } from './unirse-grupo/unirse-grupo';
import { GruposRoutingModule } from './grupos-routing-module';

@NgModule({
    declarations: [
        CrearGrupoComponent,
        UnirseGrupoComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        RouterModule,
        GruposRoutingModule
    ]
})
export class GruposModule { }