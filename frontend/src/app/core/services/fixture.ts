import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environments';

export interface Equipo {
  id: number;
  nombre: string;
  codigo_fifa: string;
  grupo: string;
  escudo: string | null;
}

export interface Partido {
  id: number;
  equipo_local: Equipo;
  equipo_visitante: Equipo;
  fecha_hora: string;
  jornada: number;
  grupo: string;
  estadio: string;
  goles_local: number | null;
  goles_visitante: number | null;
  estado: 'PENDIENTE' | 'EN_JUEGO' | 'FINALIZADO';
  bloqueado: boolean;
}

export type FixtureGrupos = {
  [grupo: string]: {
    [jornada: string]: Partido[];
  };
};

@Injectable({ providedIn: 'root' })
export class FixtureService {
  private apiUrl = `${environment.apiUrl}/fixture`;

  constructor(private http: HttpClient) { }

  getFixtureGrupos(): Observable<FixtureGrupos> {
    return this.http.get<FixtureGrupos>(`${this.apiUrl}/grupos/`);
  }

  getPartido(id: number): Observable<Partido> {
    return this.http.get<Partido>(`${this.apiUrl}/partidos/${id}/`);
  }
}