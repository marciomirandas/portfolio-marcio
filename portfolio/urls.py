from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from principal.views import *
from cursos.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')),
    path('tarefas/', include('tarefas.urls')),
    path('conteudo/', include('conteudo.urls')),
    path('api/v1/', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('usuarios/', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = error403
handler404 = error404
handler500 = error500