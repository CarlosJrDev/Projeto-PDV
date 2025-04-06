import os
import django
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cozinha.routing
import caixa.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cozinha.routing.websocket_urlpatterns +
            caixa.routing.websocket_urlpatterns
        )
    ),
})
