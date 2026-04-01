import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AuthRoutingModule } from './auth-routing-module';
import { LoginComponent } from './login/login';
import { RegistroComponent } from './registro/registro';

@NgModule({
  declarations: [LoginComponent, RegistroComponent],
  imports: [CommonModule, FormsModule, RouterModule, AuthRoutingModule]
})
export class AuthModule { }