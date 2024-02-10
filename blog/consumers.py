import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        await self.channel_layer.group_add(f'user_{user_id}', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        user_id = self.scope['user'].id
        await self.channel_layer.group_discard(f'user_{user_id}', self.channel_name)

    async def post_published(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'post_notification',
            'message': message
        }))
