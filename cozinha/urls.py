from django.urls import path
from . import views
from .views import cozinha, atualizar_status

urlpatterns = [
    path("", cozinha, name="cozinha"),
    path("pedidos/json/", views.pedidos_json, name="pedidos_json"),
    path("pedidos/<int:pedido_id>/atualizar_status/", views.atualizar_status, name="atualizar_status"),
]