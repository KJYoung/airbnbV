from django.db import models
from core import models as core_models


class Conversation(core_models.AbstractTimeStampedModel):
    """Conversation model definition"""

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        username = ", ".join(usernames)
        return username
        # return f"conversation created at {self.created}"

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "#messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "#participants"


class Message(core_models.AbstractTimeStampedModel):
    """Message model definition"""

    text = models.TextField()
    user = models.ForeignKey(
        "users.user", related_name="messages", on_delete=models.SET_NULL, null=True
    )
    Conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} : {self.text}"
