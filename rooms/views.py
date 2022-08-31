from django.utils import timezone
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django_countries import countries

from . import models, forms


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


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/room_detail.html", context={"room": room})
#     except:
#         raise Http404()  # raise not return.
#         # return redirect(reverse("core:home"))


class RoomSearch(View):
    def get(self, request):
        try:
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                rooms = models.Room.objects.all()
                filter_args = {}

                if city != "Anywhere" and city != "":
                    filter_args["city__startswith"] = city
                if country != "":
                    filter_args["country"] = country
                if room_type is not None:
                    filter_args["room_type"] = room_type
                if price is not None:
                    filter_args["price__lte"] = price
                if guests is not None:
                    filter_args["guests__gte"] = guests
                if beds is not None:
                    filter_args["beds__gte"] = beds
                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms
                if baths is not None:
                    filter_args["baths__gte"] = baths
                if instant_book:
                    filter_args["instant_book"] = True
                if superhost:
                    filter_args["host__superhost"] = True

                for selected_amen in amenities:
                    rooms = rooms.filter(amenities=selected_amen)

                for selected_fcil in facilities:
                    rooms = rooms.filter(facilities=selected_fcil)

                qs = rooms.filter(**filter_args).order_by("-created")
                # print(filter_args)
                # print(qs)
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
            else:
                rooms = models.Room.objects.all()
            # print(rooms)
            return render(
                request,
                "rooms/room_search.html",
                {"form": form, "rooms": rooms},
            )
        except:
            raise Http404()  # raise not return.
