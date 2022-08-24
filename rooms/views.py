from django.shortcuts import render
from datetime import datetime
from . import models

# from django.http import HttpResponse


def all_rooms(request):
    # return HttpResponse(content="Hello")
    now = datetime.now()
    myName = "VKJYoung"
    superMode = True

    all_rooms = models.Room.objects.all()
    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
        },
    )
