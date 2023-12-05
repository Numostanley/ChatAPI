from django.db import models
from users.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
