from pyexpat import model
from django.db import models
from core import models as core_models


class Review(core_models.AbstractTimeStampedModel):
    """Review model definition"""

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()

    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.SET_NULL, null=True
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username}'s review on {self.room.name}"
        # return self.user.username + "'s review about " + self.room.name

    def rating_average(self):
        avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6.0
        return round(avg, 2)

    rating_average.short_description = "Avg."
