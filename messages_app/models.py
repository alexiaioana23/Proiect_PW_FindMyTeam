from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):

    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return ", ".join(
            [
                user.username
                for user in self.participants.all()
            ]
        )

    @property
    def unread_count(self):

        return self.messages.filter(
            is_read=False
        ).count()


class Message(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.sender}: {self.content[:20]}'