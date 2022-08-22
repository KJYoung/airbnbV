from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Conversation admin definition"""

    list_display = ("__str__", "created", "count_participants", "count_messages")


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin definition"""

    list_display = ("__str__", "created")
