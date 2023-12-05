from rest_framework import serializers

from chat.entity.models import ChatRoom, Message
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class ChatRepository:
    @staticmethod
    def create_chatroom(name, members):
        chatroom = ChatRoom.objects.create(name=name)
        chatroom.members.set(members)
        return chatroom

    @staticmethod
    def get_chatrooms():
        return ChatRoom.objects.all()

    @staticmethod
    def leave_chatroom(chatroom_id, user_id):
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            user = User.objects.get(id=user_id)
            if chatroom.members.filter(username=user.username).exists():
                chatroom.members.remove(user)
            else:
                pass
        except ObjectDoesNotExist:
            pass

    @staticmethod
    def enter_chatroom(chatroom_id, user_id):
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            if chatroom.members.count() >= 20:
                raise serializers.ValidationError({
                    "success": False,
                    "message": "Maximum room members reached"
                })
            user = User.objects.get(id=user_id)
            if chatroom.members.filter(username=user.username).exists():
                raise serializers.ValidationError({
                    "success": False,
                    "message": "User already in this chat room"
                })
            chatroom.members.add(user)
        except ObjectDoesNotExist:
            pass

    @staticmethod
    def send_message(chatroom_id, sender_id, content, attachment):
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            sender = User.objects.get(id=sender_id)
            message = Message.objects.create(chat_room=chatroom, sender=sender, content=content, attachment=attachment)
            return message
        except ObjectDoesNotExist:
            pass

    @staticmethod
    def list_messages(chatroom_id):
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            return Message.objects.filter(chat_room=chatroom)
        except ObjectDoesNotExist:
            pass
