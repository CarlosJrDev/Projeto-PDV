from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import cozinha.routing
import caixa.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cozinha.routing.websocket_urlpatterns + caixa.routing.websocket_urlpatterns
        )
    ),
})
