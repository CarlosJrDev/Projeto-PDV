from django.contrib import admin
from .models import Restaurante, Mesa, Produto
from django.utils.html import format_html

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ("nome", "dono", "cnpj") #exibe essas colunas na listagem
    search_fields = ("nome", "cnpj") #adiciona busca por nome e cnpj

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ("numero", "restaurante", "id", "qr_code") #exibe numero da mesa e restaurante
    search_fields = ("numero",) #permite buscar pelo numero da mesa

    def qr_code_display(self, obj):
        if obj.qr_code:
            return format_html(f'<img src=""{obj.qr_code.url}" width=""100px"/>')
        return "Sem QR Code"
    
    qr_code_display.short_description = "QR Code"


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'categoria')
    search_fields = ('nome', 'categoria')