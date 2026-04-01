from django.urls import path
from .views import PronosticoListCreateView, PronosticoUpdateView, ranking_global, ranking_grupo

urlpatterns = [
    path('',                                  PronosticoListCreateView.as_view()),
    path('<int:pk>/',                         PronosticoUpdateView.as_view()),
    path('ranking/global/',                   ranking_global),
    path('ranking/grupo/<int:grupo_id>/',     ranking_grupo),
]
