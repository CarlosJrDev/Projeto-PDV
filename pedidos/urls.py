
from django.urls import path
from . import views
from .views import salvar_cliente_mesa

urlpatterns = [
    path('mesa/<int:mesa_id>/produtos/', views.listar_produtos, name='listar_produtos'),
    path('adicionar/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path("ver-carrinho/<int:mesa_id>/", views.ver_carrinho, name="ver_carrinho"),
    path("remover-item/<int:item_id>/", views.remover_do_carrinho, name="remover_do_carrinho"),
    path("finalizar-pedido/<int:mesa_id>/", views.finalizar_pedido, name="finalizar_pedido"),
    path('cliente/salvar/', salvar_cliente_mesa, name='salvar_cliente_mesa'),
]
