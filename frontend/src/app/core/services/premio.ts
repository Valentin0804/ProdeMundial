import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class PremioService {
  private apiUrl = 'http://localhost:8000/api/premios';

  constructor(private http: HttpClient) { }

  getPronostico(): Observable<any> {
    return this.http.get(`${this.apiUrl}/`);
  }

  getCandidatos(): Observable<any> {
    return this.http.get(`${this.apiUrl}/candidatos/`);
  }

  guardarPronostico(data: any): Observable<any> {
    return this.http.patch(`${this.apiUrl}/`, data);
  }

  getPronosticoUsuario(): Observable<any> {
    return this.http.get(`${this.apiUrl}/`);
  }
}