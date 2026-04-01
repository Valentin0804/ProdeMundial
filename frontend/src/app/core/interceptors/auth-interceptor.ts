import { Injectable } from '@angular/core';
import {
  HttpInterceptor, HttpRequest,
  HttpHandler, HttpEvent, HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError, BehaviorSubject } from 'rxjs';
import { catchError, filter, switchMap, take } from 'rxjs/operators';
import { AuthService } from '../services/auth';
import { Router } from '@angular/router';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  private refreshando = false;
  private refreshSubject = new BehaviorSubject<string | null>(null);

  constructor(private auth: AuthService, private router: Router) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.auth.getAccessToken();
    const reqConToken = token ? this.agregarToken(req, token) : req;

    return next.handle(reqConToken).pipe(
      catchError(err => {
        if (err instanceof HttpErrorResponse && err.status === 401) {
          return this.manejarError401(req, next);
        }
        return throwError(() => err);
      })
    );
  }

  private agregarToken(req: HttpRequest<any>, token: string) {
    return req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  private manejarError401(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (this.refreshando) {
      return this.refreshSubject.pipe(
        filter(t => t !== null),
        take(1),
        switchMap(token => next.handle(this.agregarToken(req, token!)))
      );
    }

    this.refreshando = true;
    this.refreshSubject.next(null);

    return this.auth.refreshToken().pipe(
      switchMap(res => {
        this.refreshando = false;
        this.refreshSubject.next(res.access);
        return next.handle(this.agregarToken(req, res.access));
      }),
      catchError(err => {
        this.refreshando = false;
        this.auth.logout();
        this.router.navigate(['/auth/login']);
        return throwError(() => err);
      })
    );
  }
}