from math import ceil
from django.shortcuts import render
from datetime import datetime
from . import models

# from django.http import HttpResponse


def all_rooms(request):
    try:
        pageNum = int(request.GET.get("page", 1))
        if pageNum <= 0:
            raise RuntimeError()
    except:
        pageNum = 1
    try:
        pageSize = int(request.GET.get("page_size", 10))
        if pageSize <= 0:
            raise RuntimeError()
    except:
        pageSize = 10

    offset = (pageNum - 1) * pageSize
    limit = pageNum * pageSize

    all_rooms = models.Room.objects.all()[offset:limit]

    # Total page number calculation.
    totalRoom = models.Room.objects.count()
    pageTotal = ceil(totalRoom / pageSize)

    return render(
        request,
        "rooms/home.html",
        context={
            "rooms": all_rooms,
            "pageNum": pageNum,
            "pageTotal": pageTotal,
            "pageRange": range(1, pageTotal + 1),
            "pageSize": pageSize,
        },
    )
