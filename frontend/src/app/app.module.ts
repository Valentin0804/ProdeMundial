import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app';
import { SharedModule } from './shared/shared-module';
import { routes } from './app.routes';
import { jwtInterceptor } from './interceptors/jwt-interceptor';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

@NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        SharedModule,
        RouterModule.forRoot(routes)
    ],
    providers: [
        provideHttpClient(withInterceptors([jwtInterceptor]))
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }