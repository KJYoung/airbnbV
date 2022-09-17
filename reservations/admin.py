from django.contrib import admin
from . import models


@admin.register(models.BookedDay)
class BookedDayAdmin(admin.ModelAdmin):
    """Booked day admin definition"""

    list_display = ("day", "reservation", "created")
    pass


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """Reservation admin definition"""

    list_display = (
        "id",
        "room",
        "status",
        "check_in",
        "check_out",
        "guest",
        "is_in_progress",
        "is_finished",
    )

    list_filter = ("status",)
