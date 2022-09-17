import datetime
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from . import models
from reviews import forms as review_forms
from rooms import models as room_models


class AlreadyBookedException(Exception):
    pass


def createReservation(request, room_pk, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room_pk)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise AlreadyBookedException()
    except (room_models.Room.DoesNotExist, AlreadyBookedException):
        messages.error(request, "Can't book that room at that time.")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
        print("Hi")
    print(room_pk, year, month, day)


class ReservationDetail(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation:
            raise Http404()
        elif (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        else:
            form = review_forms.CreateReviewForm()
            return render(
                self.request,
                "reservations/detail.html",
                {"reservation": reservation, "form": form},
            )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation:
        # no reservation
        raise Http404()
    elif reservation.guest != request.user and reservation.room.host != request.user:
        raise Http404()
    else:
        if verb == "confirm":
            reservation.status = models.Reservation.STATUS_CONFIRMED
        elif verb == "cancel":
            reservation.status = models.Reservation.STATUS_CANCELED
            models.BookedDay.objects.filter(reservation=reservation).delete()
        reservation.save()
        messages.success(request, "Reservation updated!")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
