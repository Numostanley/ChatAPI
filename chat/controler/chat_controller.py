from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from chat.service.chat_service import ChatService
from chat.entity.serializers import ChatRoomSerializer, MessageSerializer


class ChatroomView(APIView):
    def get(self, request):
        chat_service = ChatService()
        chatrooms = chat_service.get_chatrooms()
        serializer = ChatRoomSerializer(chatrooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = self.request.data
        name = data.get('name')
        members = data.get('members', [])

        chat_service = ChatService()
        chatroom = chat_service.create_chatroom(name, members)

        serializer = ChatRoomSerializer(chatroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def leave_chatroom(request, chatroom_id):
    user_id = request.user.id
    chat_service = ChatService()
    chat_service.leave_chatroom(chatroom_id, user_id=user_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def enter_chatroom(request, chatroom_id):
    user_id = request.user.id
    chat_service = ChatService()
    chat_service.enter_chatroom(chatroom_id, user_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def send_message(request, chatroom_id):
    data = request.data
    sender_id = request.user.id
    content = data.get('message')
    attachment = request.FILES.get('attachment', None)

    chat_service = ChatService()
    message = chat_service.send_message(chatroom_id, sender_id, content, attachment)

    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def list_messages(request, chatroom_id):
    chat_service = ChatService()
    messages = chat_service.list_messages(chatroom_id)
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
