from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.AbstractTimeStampedModel):
    """Reservation Model Definition"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=16, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()

    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room.name} : {self.check_in} ~ {self.check_out}"

    def is_in_progress(self):
        now = timezone.now().date()
        print("check in :", self.check_in)
        print("check out :", self.check_out)
        print("now > self.check_in", now > self.check_in)
        print("now < self.check_out", now < self.check_out)
        return (now >= self.check_in) and (now <= self.check_out)

    is_in_progress.boolean = True
    is_in_progress.short_description = "In progress"

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True
    is_finished.short_description = "Finished"
