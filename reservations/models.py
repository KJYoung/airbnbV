import datetime
from django.db import models
from django.utils import timezone
from core import models as core_models
from . import managers


class BookedDay(core_models.AbstractTimeStampedModel):
    day = models.DateField(default=timezone.now)
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = "Booked day"
        verbose_name_plural = "Booked days"


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

    objects = managers.CustomReservateionManager()

    def __str__(self):
        return f"{self.room.name} : {self.check_in} ~ {self.check_out}"

    def is_in_progress(self):
        now = timezone.now().date()
        # print("check in :", self.check_in)
        # print("check out :", self.check_out)
        # print("now > self.check_in", now > self.check_in)
        # print("now < self.check_out", now < self.check_out)
        return (now >= self.check_in) and (now <= self.check_out)

    is_in_progress.boolean = True
    is_in_progress.short_description = "In progress"

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished

    is_finished.boolean = True
    is_finished.short_description = "Finished"

    def save(self, *args, **kwargs):
        if self.pk is None:
            # New one.
            start, end = self.check_in, self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                reservation__room=self.room, day__range=(start, end)
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    print(day)
                    BookedDay.objects.create(day=day, reservation=self)
        else:
            # Existing one.
            return super().save(*args, **kwargs)
