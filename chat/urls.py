from django.urls import path
from .views import ChatroomView, leave_chatroom, enter_chatroom, send_message, list_messages

urlpatterns = [
    path('chat_room', ChatroomView.as_view()),
    path('leave_room/<chatroom_id>', leave_chatroom),
    path('enter_room/<chatroom_id>', enter_chatroom),
    path('send_message/<chatroom_id>', send_message),
    path('messages/<chatroom_id>', list_messages)
]
