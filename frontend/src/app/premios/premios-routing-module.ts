import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PremiosForm } from './premios-form/premios-form';

const routes: Routes = [
  { path: '', component: PremiosForm }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PremiosRoutingModule { }