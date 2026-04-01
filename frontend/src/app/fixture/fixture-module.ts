import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FixtureRoutingModule } from './fixture-routing-module';
import { FixtureGruposComponent } from './fixture-grupos/fixture-grupos';
import { PartidoCard } from './partido-card/partido-card';
import { GrupoCard } from './grupo-card/grupo-card';

@NgModule({
  declarations: [FixtureGruposComponent],
  imports: [
    CommonModule,
    FormsModule,
    FixtureRoutingModule,
    GrupoCard,
    PartidoCard,

  ]
})
export class FixtureModule { }