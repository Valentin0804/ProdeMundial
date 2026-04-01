import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-navbar',
  standalone: false,
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.scss']
})
export class NavbarComponent implements OnInit {
  usuario = '';
  menuAbierto = false;

  constructor(public auth: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.usuario = this.auth.getUsuarioActual();
  }

  logout(): void {
    this.auth.logout();
  }

  toggleMenu(): void {
    this.menuAbierto = !this.menuAbierto;
  }
}