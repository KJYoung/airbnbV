from django.db.models import Q
from django.http import Http404
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse
from users import models as user_models
from . import models, forms
import conversations

# Create your views here.
def go_conversation(request, user1_pk, user2_pk):
    user1 = user_models.User.objects.get_or_none(pk=user1_pk)
    user2 = user_models.User.objects.get_or_none(pk=user2_pk)
    if (user1 is not None) and (user2 is not None) and (user1 != user2):
        conversation = models.Conversation.objects.get_or_none(
            Q(participants=user1) & Q(participants=user2)
        )
        if conversation is not None:
            pass
        else:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user1, user2)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))
    else:
        pass


class ConversationDetailView(View):
    model = models.Conversation

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if conversation is not None:
            form = forms.AddMessageForm()
            return render(
                self.request,
                "conversations/conversation_detail.html",
                {"conversation": conversation, "form": form},
            )
        else:
            raise Http404()

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        # TODO: if self.request.user is not in the conversation__participants.
        if (message is not None) and (conversation is not None):
            models.Message.objects.create(
                text=message, user=self.request.user, Conversation=conversation
            )
        else:
            pass
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
        form = forms.AddMessageForm(self.request.POST)
