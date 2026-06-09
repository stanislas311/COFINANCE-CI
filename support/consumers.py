import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'support_{self.conversation_id}'

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
        message_type = data.get('type', 'message')

        if message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'user_id': data.get('user_id'),
                    'is_typing': data.get('is_typing', False),
                }
            )
        else:
            message = await self.save_message(data)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': message['id'],
                    'contenu': message['contenu'],
                    'expediteur_id': message['expediteur_id'],
                    'expediteur_nom': message['expediteur_nom'],
                    'timestamp': message['timestamp'],
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'id': event['id'],
            'contenu': event['contenu'],
            'expediteur_id': event['expediteur_id'],
            'expediteur_nom': event['expediteur_nom'],
            'timestamp': event['timestamp'],
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user_id': event['user_id'],
            'is_typing': event['is_typing'],
        }))

    @database_sync_to_async
    def save_message(self, data):
        from .models import Conversation, Message
        from accounts.models import User

        conversation = Conversation.objects.get(id=self.conversation_id)
        user = User.objects.get(id=data['user_id'])
        message = Message.objects.create(
            conversation=conversation,
            expediteur=user,
            contenu=data['contenu']
        )
        return {
            'id': message.id,
            'contenu': message.contenu,
            'expediteur_id': user.id,
            'expediteur_nom': user.get_full_name() or user.username,
            'timestamp': message.timestamp.isoformat(),
        }