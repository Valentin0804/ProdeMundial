import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environments';

@Injectable({ providedIn: 'root' })
export class GrupoService {
    private apiUrl = `${environment.apiUrl}/auth/grupos/`;
    constructor(private http: HttpClient) { }

    getMisGrupos(): Observable<any[]> {
        return this.http.get<any[]>(this.apiUrl);
    }

    crearGrupo(nombre: string): Observable<any> {
        return this.http.post<any>(this.apiUrl, { nombre });
    }

    unirseAGrupo(codigo: string): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}unirse/`, {
            codigo_invitacion: codigo
        });
    }

    getDetalleModal(grupoId: number): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}${grupoId}/detalle-modal/`);
    }

    eliminarMiembro(grupoId: number, usuarioId: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}${grupoId}/miembros/${usuarioId}/`);
    }

    salirDelGrupo(grupoId: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}${grupoId}/salir/`);
    }
}