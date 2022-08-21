from django.db import models
from core import models as core_models


class Conversation(core_models.AbstractTimeStampedModel):
    """Conversation model definition"""

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        return f"conversation created at {self.created}"


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
