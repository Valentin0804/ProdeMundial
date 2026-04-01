import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CrearGrupoComponent } from './crear-grupo/crear-grupo';

const routes: Routes = [
    { path: 'crear', component: CrearGrupoComponent },
    // Aquí podrías agregar después: { path: 'lista', component: ListaGruposComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class GruposRoutingModule { }