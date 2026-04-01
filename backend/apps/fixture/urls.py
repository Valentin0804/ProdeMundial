from django.urls import path
from .views import EquipoListView, JugadorListView, fixture_grupos, PartidoDetailView

urlpatterns = [
    path('equipos/',          EquipoListView.as_view()),
    path('jugadores/',        JugadorListView.as_view()),
    path('grupos/',           fixture_grupos),
    path('partidos/<int:pk>/',PartidoDetailView.as_view()),
]
