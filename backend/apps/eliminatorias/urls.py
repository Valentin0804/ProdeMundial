from django.urls import path
from .views import bracket_usuario, PronosticoElimListCreateView, PronosticoElimUpdateView

urlpatterns = [
    path('bracket/',                  bracket_usuario),
    path('bracket/<int:usuario_id>/', bracket_usuario),
    path('pronosticos/',              PronosticoElimListCreateView.as_view()),
    path('pronosticos/<int:pk>/',     PronosticoElimUpdateView.as_view()),
]
