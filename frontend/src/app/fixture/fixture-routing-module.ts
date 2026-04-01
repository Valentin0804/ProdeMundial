import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FixtureGruposComponent } from './fixture-grupos/fixture-grupos';

const routes: Routes = [
  { path: '', component: FixtureGruposComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FixtureRoutingModule { }