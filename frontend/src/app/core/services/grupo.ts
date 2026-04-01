import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environments';

@Injectable({ providedIn: 'root' })
export class GrupoService {
    // Ajustá esto según tu urls.py (probablemente /api/usuarios/grupos/)
    private apiUrl = `${environment.apiUrl}/auth/grupos/`;

    constructor(private http: HttpClient) { }

    // GET: Listar mis grupos
    getMisGrupos(): Observable<any[]> {
        return this.http.get<any[]>(this.apiUrl);
    }

    // POST: Crear grupo
    crearGrupo(nombre: string): Observable<any> {
        return this.http.post<any>(this.apiUrl, { nombre });
    }

    // POST: Unirse con código
    unirseAGrupo(codigo: string): Observable<any> {
        // Apunta a la función unirse_grupo de tu views.py
        return this.http.post<any>(`${environment.apiUrl}/usuarios/unirse-grupo/`, {
            codigo_invitacion: codigo
        });
    }
}