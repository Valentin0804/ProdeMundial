import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BracketView } from './bracket-view/bracket-view';

const routes: Routes = [
  { path: '', component: BracketView }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BracketRoutingModule { }