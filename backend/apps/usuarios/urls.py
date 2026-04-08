from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegistroView, PerfilView,
    GrupoPrivadoListCreateView, unirse_grupo, MiembrosGrupoView,
    detalle_grupo_modal, eliminar_miembro, salir_grupo
)

urlpatterns = [
    path('registro/',           RegistroView.as_view()),
    path('login/',              TokenObtainPairView.as_view()),
    path('token/refresh/',      TokenRefreshView.as_view()),
    path('perfil/',             PerfilView.as_view()),
    path('grupos/',             GrupoPrivadoListCreateView.as_view()),
    path('grupos/unirse/',      unirse_grupo),
    path('grupos/<int:grupo_id>/miembros/', MiembrosGrupoView.as_view()),
    path('grupos/<int:grupo_id>/detalle-modal/', detalle_grupo_modal),
    path('grupos/<int:grupo_id>/miembros/<int:usuario_id>/', eliminar_miembro),
    path('grupos/<int:grupo_id>/salir/', salir_grupo),
]