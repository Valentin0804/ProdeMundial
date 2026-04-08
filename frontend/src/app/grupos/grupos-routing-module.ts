import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CrearGrupoComponent } from './crear-grupo/crear-grupo';
import { UnirseGrupoComponent } from './unirse-grupo/unirse-grupo';

const routes: Routes = [
    { path: 'crear', component: CrearGrupoComponent },
    { path: 'unirse', component: UnirseGrupoComponent },

];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class GruposRoutingModule { }