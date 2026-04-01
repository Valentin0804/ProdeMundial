import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth';

@Component({
  selector: 'app-registro',
  standalone: false,
  templateUrl: './registro.html',
  styleUrls: ['./registro.scss']
})
export class RegistroComponent {
  form = {
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    password2: ''
  };
  cargando = false;
  error = '';
  exito = false;

  constructor(private auth: AuthService, private router: Router) { }

  registrar(): void {
    if (!this.form.username || !this.form.password || !this.form.password2) {
      this.error = 'Completá los campos obligatorios.';
      return;
    }
    if (this.form.password !== this.form.password2) {
      this.error = 'Las contraseñas no coinciden.';
      return;
    }
    this.cargando = true;
    this.error = '';

    this.auth.registro(this.form).subscribe({
      next: () => {
        this.auth.login(this.form.username, this.form.password).subscribe({
          next: () => this.router.navigate(['/fixture']),
          error: () => this.router.navigate(['/auth/login'])
        });
      },
      error: (err) => {
        const data = err.error;
        if (data?.username) this.error = 'Ese nombre de usuario ya existe.';
        else if (data?.password) this.error = data.password[0];
        else this.error = 'Error al registrarse. Intentá de nuevo.';
        this.cargando = false;
      }
    });
  }
}