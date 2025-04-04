
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("cozinha/", include("cozinha.urls")),
    path("pedidos/", include("pedidos.urls")),
    path('caixa/', include('caixa.urls')),

]
