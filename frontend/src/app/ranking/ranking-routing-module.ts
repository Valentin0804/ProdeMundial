import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TablaGlobal } from './tabla-global/tabla-global';

const routes: Routes = [
  { path: '', component: TablaGlobal }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RankingRoutingModule { }