
from django.urls import path
from . import views

urlpatterns = [
    path("mesa/<int:mesa_id>/produtos/", views.listar_produtos, name="listar_produtos"),
    path("adicionar-ao-carrinho/<int:produto_id>/<int:mesa_id>/", views.adicionar_ao_carrinho, name="adicionar_ao_carrinho"),
    path("ver-carrinho/<int:mesa_id>/", views.ver_carrinho, name="ver_carrinho"),
    path("remover-item/<int:item_id>/", views.remover_do_carrinho, name="remover_do_carrinho"),
    path("finalizar-pedido/<int:mesa_id>/", views.finalizar_pedido, name="finalizar_pedido"),
]
