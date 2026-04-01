import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { NavbarComponent } from './navbar/navbar';
import { Loading } from './loading/loading';

@NgModule({
  declarations: [NavbarComponent],
  imports: [CommonModule, RouterModule, Loading],
  exports: [NavbarComponent, Loading]
})
export class SharedModule { }