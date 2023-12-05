from rest_framework import serializers

from users.serializers import UserSerializer
from .models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    chat_room = ChatRoomSerializer()

    class Meta:
        model = Message
        fields = '__all__'
