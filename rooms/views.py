from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect

from django_countries import countries

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


def room_search(request):
    try:
        city = request.GET.get("city", "Seoul")
        city = str.capitalize(city)
        country = request.GET.get("country", "KR")
        room_type = int(request.GET.get("room_types", 0))
        price = int(request.GET.get("price", 0))
        guests = int(request.GET.get("guests", 0))
        beds = int(request.GET.get("beds", 0))
        bedrooms = int(request.GET.get("bedrooms", 0))
        baths = int(request.GET.get("baths", 0))
        instant = request.GET.get("instant", False)
        superhost = request.GET.get("superhost", False)

        s_amenities = request.GET.getlist("amenities")
        s_facilities = request.GET.getlist("facilities")

        room_types = models.RoomType.objects.all()
        amenities = models.Amenity.objects.all()
        facilities = models.Facility.objects.all()

        form = {
            "selected_city": city,
            "selected_country": country,
            "selected_room_type": room_type,
            "selected_price": price,
            "selected_guests": guests,
            "selected_beds": beds,
            "selected_bedrooms": bedrooms,
            "selected_baths": baths,
            "selected_amen": s_amenities,
            "selected_fcil": s_facilities,
            "selected_instant": instant,
            "selected_superhost": superhost,
        }
        choices = {
            "countries": countries,
            "room_types": room_types,
            "amenities": amenities,
            "facilities": facilities,
        }
        return render(
            request,
            "rooms/room_search.html",
            {**form, **choices},
        )
    except:
        raise Http404()  # raise not return.


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
