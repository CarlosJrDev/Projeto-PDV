

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.mesa_id = self.scope['url_route']['kwargs']['mesa_id']
        self.room_group_name = f'mesa_{self.mesa_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'pedido_status',
                'message': data['message']
            }
        )

    async def pedido_status(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
