import { HttpInterceptorFn } from '@angular/common/http';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  // 1. Buscamos el nombre EXACTO que pusiste en el AuthService
  const token = localStorage.getItem('access_token');

  // 2. Si el token existe, clonamos la petición
  if (token) {
    const cloned = req.clone({
      setHeaders: {
        // Importante: Chequeá que en Django uses SimpleJWT (usa Bearer)
        Authorization: `Bearer ${token}`
      }
    });
    return next(cloned);
  }

  // 3. Si no hay token, la petición sigue su curso (ej: para el login)
  return next(req);
};