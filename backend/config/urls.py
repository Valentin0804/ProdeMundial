from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/',         include('apps.usuarios.urls')),
    path('api/fixture/',      include('apps.fixture.urls')),
    path('api/pronosticos/',  include('apps.pronosticos.urls')),
    path('api/eliminatorias/',include('apps.eliminatorias.urls')),
    path('api/premios/',      include('apps.premios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
