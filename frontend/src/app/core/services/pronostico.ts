import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environments';

export interface Pronostico {
  id?: number;
  partido: number;
  goles_local: number;
  goles_visitante: number;
  puntos_obtenidos?: number | null;
  bloqueado?: boolean;
}

export interface RankingItem {
  posicion: number;
  usuario: string;
  avatar?: string | null;
  puntos_totales: number;
  exactos: number;
  acertados: number;
  jugados: number;
}

@Injectable({ providedIn: 'root' })
export class PronosticoService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getMisPronosticos(): Observable<Pronostico[]> {
    return this.http.get<Pronostico[]>(`${this.apiUrl}/pronosticos/`);
  }

  crearPronostico(data: Pronostico): Observable<Pronostico> {
    return this.http.post<Pronostico>(`${this.apiUrl}/pronosticos/`, data);
  }

  editarPronostico(id: number, data: Partial<Pronostico>): Observable<Pronostico> {
    return this.http.patch<Pronostico>(`${this.apiUrl}/pronosticos/${id}/`, data);
  }

  guardarOActualizar(pronosticos: Map<number, Pronostico>, partidoId: number, gl: number, gv: number): Observable<Pronostico> {
    const existente = pronosticos.get(partidoId);
    if (existente?.id) {
      return this.editarPronostico(existente.id, { goles_local: gl, goles_visitante: gv });
    }
    return this.crearPronostico({ partido: partidoId, goles_local: gl, goles_visitante: gv });
  }

  getRankingGlobal(): Observable<RankingItem[]> {
    return this.http.get<RankingItem[]>(`${this.apiUrl}/pronosticos/ranking/global/`);
  }

  getRankingGrupo(grupoId: number): Observable<RankingItem[]> {
    return this.http.get<RankingItem[]>(`${this.apiUrl}/pronosticos/ranking/grupo/${grupoId}/`);
  }
}