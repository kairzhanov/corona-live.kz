import { Injectable, Optional, Inject } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable } from 'rxjs';
import {Request} from 'express';
import {REQUEST} from '@nguniversal/express-engine/tokens';


@Injectable()
export class UniversalInterceptor implements HttpInterceptor {
  
  constructor(@Optional() @Inject(REQUEST) protected request?: Request) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    let serverReq: HttpRequest<unknown> = request
    if (this.request) {
      let newUrl = `${this.request.protocol}://${this.request.get('host')}`;
      if (!request.url.startsWith('/')) {
        newUrl += '/';
      }
      newUrl += request.url;
      serverReq = request.clone({url: newUrl});
    }
    return next.handle(serverReq);
  }
}
