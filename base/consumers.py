from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef

from .models import Room, Message
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    def get_message_data(self, user_id, room_id, message, replied_to=None):
        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=room_id)

        room.participants.add(user)

        message_data = {
            'user': user,
            'room': room,
            'body': message,
        }

        if replied_to:
            try:
                replied_msg = Message.objects.get(id=replied_to)
                message_data['replied_msg'] = replied_msg
            except Message.DoesNotExist:
                pass

        message = Message.objects.create(**message_data)

        return {
            'id': message.id,
            'user': message.user.username,
            'user_id': message.user.id,
            'body': message.body,
            'created': message.created.strftime("%Y-%m-%d %H:%M:%S"),
            'replied_to': {
                'id': message.replied_msg.id,
                'body': message.replied_msg.body,
            } if hasattr(message, 'replied_msg') and message.replied_msg else None
        }

    @database_sync_to_async
    def save_message(self, user_id, room_id, message, replied_to=None):
        try:
            return self.get_message_data(user_id, room_id, message, replied_to)
        except (User.DoesNotExist, Room.DoesNotExist):
            return None

    @database_sync_to_async
    def get_participants(self, room_id):
        room = Room.objects.get(id=room_id)
        # return list(room.participants.values('id', 'username').order_by('username')) --- ordering by username

        # ordering by whoever first send msg
        return list(room.participants.annotate(
            first_message_time=Subquery(
                Message.objects.filter(
                    user_id=OuterRef('id'),
                    room_id=room_id
                ).values('created').order_by('created')[:1]
            )
        ).order_by('first_message_time', 'username').values('id', 'username'))

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            replied_to = data.get('replied_to')

            message_data = await self.save_message(
                self.user.id,
                self.room_id,
                message,
                replied_to
            )

            if message_data:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message_data
                    }
                )

                participants = await self.get_participants(self.room_id)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'participants_update',
                        'participants': participants,
                    }
                )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))

    async def participants_update(self, event):
        await self.send(text_data=json.dumps({
            'participants': event['participants']
        }))
