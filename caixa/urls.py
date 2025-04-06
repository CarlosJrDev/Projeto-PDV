from django.urls import path
from .views import caixa, detalhe_pagamento, detalhe_pedido, gerar_comprovante, confirmacao_pagamento

urlpatterns = [
    path('', caixa, name="caixa"),
    path("pedido/<int:pedido_id>/", detalhe_pedido, name="detalhe_pedido"),
    path('detalhe_pagamento/<int:pedido_id>/', detalhe_pagamento, name="detalhe_pagamento"),
    path("confirmacao-pagamento/<int:pedido_id>/", confirmacao_pagamento, name="confirmacao_pagamento"),
    path('caixa/comprovante/<int:pedido_id>/', gerar_comprovante, name='gerar_comprovante'),
]
