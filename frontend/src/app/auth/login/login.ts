import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class LoginComponent {
  username = '';
  password = '';
  cargando = false;
  error = '';

  constructor(private auth: AuthService, private router: Router) { }

  login(): void {
    if (!this.username || !this.password) {
      this.error = 'Completá todos los campos.';
      return;
    }
    this.cargando = true;
    this.error = '';

    this.auth.login(this.username, this.password).subscribe({
      next: () => this.router.navigate(['/home']),
      error: () => {
        this.error = 'Usuario o contraseña incorrectos.';
        this.cargando = false;
      }
    });
  }
}