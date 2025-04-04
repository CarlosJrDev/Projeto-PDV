from django.urls import path
from .views import cardapio

urlpatterns = [
    path("cardapio/<int:mesa_id>/", cardapio, name="cardapio"),
]
