from django.contrib import admin
from .models import Pedido, ItemPedido

@admin.register(Pedido)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'status', 'get_total', 'criado_em')  # Chamando total como método
    list_filter = ('status', 'criado_em')
    search_fields = ('mesa__numero',)

    def get_total(self, obj):
        return obj.total()  # Chamando o método total da model Pedido
    get_total.short_description = "Total"

@admin.register(ItemPedido)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'produto', 'quantidade', 'get_subtotal')
    search_fields = ('pedido__id', 'produto__nome')

    def get_subtotal(self, obj):
        return obj.subtotal()
    get_subtotal.short_description = "Subtotal"
