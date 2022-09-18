from django.contrib import messages
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from rooms import models as room_models
from . import models

# Create your views here.
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if (room is not None) and (action is not None):
        (favList, created) = models.List.objects.get_or_create(
            user=request.user, name="My Favorite Places"
        )  # If you want to extend multiple lists, you should modify this. get_or_create only deals with the one element.
        if action == "add":
            favList.rooms.add(room)
        elif action == "remove":
            favList.rooms.remove(room)
        else:
            messages.error(request, _("Can't go there!"))
            return redirect(reverse("core:home"))
        # favList.save()
        return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))
    else:
        messages.error(request, _("Can't go there!"))
        return redirect(reverse("core:home"))


class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"
    pass
