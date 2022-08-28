from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from . import models


class HomeView(ListView):
    """HomeView definition"""

    model = models.Room
    paginate_by: int = 10
    paginate_orphans: int = 5
    page_kwarg: str = "page"
    ordering = ["created"]
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class RoomDetail(DetailView):
    """RoomDetail definition"""

    model = models.Room
    pk_url_kwarg: str = "pk"


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/room_detail.html", context={"room": room})
    except:
        raise Http404()  # raise not return.
        # return redirect(reverse("core:home"))


# def all_rooms_PAGE(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)

#     try:
#         rooms = paginator.page(int(page))
#         return render(
#             request,
#             "rooms/home.html",
#             context={"page": rooms},
#         )
#     except EmptyPage:
#         return redirect("/")
#     except:  # ValueError.
#         return redirect("/")


# def all_rooms_GET_PAGE(request):
#     page = request.GET.get("page")
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     rooms = paginator.get_page(page)
#     print("Vars get_page : ", vars(rooms))
#     print("Vars paginator : ", vars(rooms.paginator))
#     return render(
#         request,
#         "rooms/home.html",
#         context={"page": rooms},
#     )
