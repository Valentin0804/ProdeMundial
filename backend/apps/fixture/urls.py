from django.urls import path
from .views import EquipoListView, JugadorListView, fixture_grupos, PartidoDetailView, proxy_foto_jugador

urlpatterns = [
    path('equipos/',          EquipoListView.as_view()),
    path('jugadores/',        JugadorListView.as_view()),
    path('grupos/',           fixture_grupos),
    path('partidos/<int:pk>/',PartidoDetailView.as_view()),
    path('jugador/foto/<int:id_externo>/', proxy_foto_jugador, name='proxy-foto'),
]
