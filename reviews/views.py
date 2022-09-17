from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
from . import forms
from rooms import models as room_models


def create_review(request, room_pk):
    if request.method == "POST":
        form = forms.CreateReviewForm(request.POST)
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        if not room:
            return redirect(reverse("core:home"))
        else:
            if form.is_valid():
                review = form.save()
                review.room = room
                review.user = request.user
                review.save()
                messages.success(request, "Review was saved!")
                return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))
            else:
                messages.error(request, "Invalid inputs")
                return redirect(reverse("core:home"))
    else:
        messages.error(request, "Invalid methods")
        return redirect(reverse("core:home"))
