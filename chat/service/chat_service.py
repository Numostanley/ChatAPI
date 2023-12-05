from chat.repository.chat_repository import ChatRepository


class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()

    def create_chatroom(self, name, members):
        return self.chat_repository.create_chatroom(name, members)

    def get_chatrooms(self):
        return self.chat_repository.get_chatrooms()

    def leave_chatroom(self, chatroom_id, user_id):
        self.chat_repository.leave_chatroom(chatroom_id, user_id)

    def enter_chatroom(self, chatroom_id, user_id):
        self.chat_repository.enter_chatroom(chatroom_id, user_id)

    def send_message(self, chatroom_id, sender_id, content, attachment):
        return self.chat_repository.send_message(chatroom_id, sender_id, content, attachment)

    def list_messages(self, chatroom_id):
        return self.chat_repository.list_messages(chatroom_id)
