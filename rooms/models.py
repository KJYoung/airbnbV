from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils import timezone
from dateutil import relativedelta

from core import models as core_models
from users import models as users_models
from cal import Calendar


class AbstractItem(core_models.AbstractTimeStampedModel):
    """Abstract Item model definition"""

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class RoomType(AbstractItem):
    """RoomType model definition"""

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):
    """Amenity model definition"""

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):
    """Facility model definition"""

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):
    """HouseRule model definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.AbstractTimeStampedModel):
    """Photo model definition"""

    caption = models.CharField(max_length=120)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.AbstractTimeStampedModel):
    """Room model definition"""

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=60)
    price = models.IntegerField()
    address = models.CharField(max_length=250)

    guests = models.IntegerField(help_text="How many people will stay?")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()

    check_in = models.TimeField()
    check_out = models.TimeField()

    instant_book = models.BooleanField(default=False)

    host = models.ForeignKey(
        users_models.User, related_name="rooms", on_delete=models.CASCADE
    )

    room_type = models.ForeignKey(
        RoomType, related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField(Amenity, related_name="rooms", blank=True)
    facilities = models.ManyToManyField(Facility, related_name="rooms", blank=True)
    house_rules = models.ManyToManyField(HouseRule, related_name="rooms", blank=True)

    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def total_rating_average(self):
        reviews = self.reviews.all()
        ratings = 0.0
        for review in reviews:
            ratings += review.rating_average()

        if len(reviews) == 0:
            total_avg = 0.0
        else:
            total_avg = ratings / len(reviews)

        return round(total_avg, 2)

    total_rating_average.short_description = "Avg. Rating"

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def get_first_photo_url(self):
        try:
            # print(self.name, self.photos.count())
            (photo,) = self.photos.all()[:1]
            # print(self.name, photo.file.url)
            return photo.file.url
        except:
            return None

    def get_four_photos(self):
        photos = self.photos.all()[1:5]
        return photos

    # def get_beds(self):
    #     if self.beds == 1:
    #         return f"{self.beds} bed"
    #     else:
    #         return f"{self.beds} beds"

    def get_calendar(self):
        """This month and Next month."""
        today = timezone.localtime(timezone.now()).date()
        nextmonth = today + relativedelta.relativedelta(months=1)

        calendar_cur = Calendar(today.year, today.month)
        calendar_nex = Calendar(nextmonth.year, nextmonth.month)
        return [calendar_cur, calendar_nex]
