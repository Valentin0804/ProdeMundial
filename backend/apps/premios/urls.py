from django.urls import path
from .views import PronosticoPremioView, candidatos_premios

urlpatterns = [
    path('', PronosticoPremioView.as_view()),
    path('candidatos/', candidatos_premios),
]
