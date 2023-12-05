import base64
import json
import secrets

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from .entity.models import Message, ChatRoom
from .entity.serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join a room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave a room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into a dictionary object
        text_data_json = json.loads(text_data)

        # Send a message to a room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    # Receive a message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )

        chat_room = ChatRoom.objects.get(id=int(self.room_name))
        sender = self.scope['user']

        # Attachment
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender=sender,
                attachment=file_data,
                content=message,
                chat_room=chat_room,
            )
        else:
            _message = Message.objects.create(
                sender=sender,
                content=message,
                chat_room=chat_room,
            )
        serializer = MessageSerializer(instance=_message)
        # Send a message to WebSocket
        self.send(
            text_data=json.dumps(
                serializer.data
            )
        )
