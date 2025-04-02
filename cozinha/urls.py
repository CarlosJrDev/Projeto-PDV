from django.urls import path
from .views import cozinha, atualizar_status

urlpatterns = [
    path("", cozinha, name="cozinha"),
    path("<int:pedido_id>/<str:novo_status>/", atualizar_status, name="atualizar_status"),
]