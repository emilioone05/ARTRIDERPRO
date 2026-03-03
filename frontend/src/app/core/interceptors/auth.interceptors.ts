import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Auth, idToken } from '@angular/fire/auth';
import { switchMap, take } from 'rxjs/operators';
import { from, of } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(Auth);

  return idToken(auth).pipe(
    take(1),
    switchMap((token) => {
      if (token) {
        const authReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`
          }
        });
        return next(authReq);
      }
      return next(req);
    })
  );
};
