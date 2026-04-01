import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'fixture',
        pathMatch: 'full'
    },
    {
        path: 'auth',
        loadChildren: () =>
            import('./auth/auth-module').then(m => m.AuthModule)
    },
    {
        path: 'fixture',
        canActivate: [authGuard],
        loadChildren: () =>
            import('./fixture/fixture-module').then(m => m.FixtureModule)
    },
    {
        path: 'bracket',
        canActivate: [authGuard],
        loadChildren: () =>
            import('./bracket/bracket-module').then(m => m.BracketModule)
    },
    {
        path: 'premios',
        canActivate: [authGuard],
        loadChildren: () =>
            import('./premios/premios-module').then(m => m.PremiosModule)
    },
    {
        path: 'ranking',
        canActivate: [authGuard],
        loadChildren: () =>
            import('./ranking/ranking-module').then(m => m.RankingModule)
    },
    {
        path: '**',
        redirectTo: 'fixture'
    }
];