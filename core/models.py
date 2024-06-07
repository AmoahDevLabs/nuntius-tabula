from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageBoard(models.Model):
    subscribers = models.ManyToManyField(User, related_name='message_board', blank=True)

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    body = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.author.username
