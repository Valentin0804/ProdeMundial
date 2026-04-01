from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegistroView, PerfilView,
    GrupoPrivadoListCreateView, unirse_grupo, MiembrosGrupoView,
)

urlpatterns = [
    path('registro/',           RegistroView.as_view()),
    path('login/',              TokenObtainPairView.as_view()),
    path('token/refresh/',      TokenRefreshView.as_view()),
    path('perfil/',             PerfilView.as_view()),
    path('grupos/',             GrupoPrivadoListCreateView.as_view()),
    path('grupos/unirse/',      unirse_grupo),
    path('grupos/<int:grupo_id>/miembros/', MiembrosGrupoView.as_view()),
]
