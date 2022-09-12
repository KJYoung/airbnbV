from dataclasses import fields
from urllib import request
from django import forms
from . import models
from django_countries.fields import CountryField


class SearchForm(forms.Form):
    # city = forms.CharField(initial="anywhere", widget=forms.Textarea)
    city = forms.CharField(initial="anywhere", required=False)
    country = CountryField(blank_label="Choose Country").formfield(required=False)
    room_type = forms.ModelChoiceField(
        empty_label="any type", required=False, queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)

    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    amenities = forms.ModelMultipleChoiceField(
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    facilities = forms.ModelMultipleChoiceField(
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("file", "caption")

    def save(self, pk, *args, **kwargs):
        new_photo = super().save(commit=False)

        room = models.Room.objects.get(pk=pk)
        new_photo.room = room

        new_photo.save()


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "instant_book",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    def save(self, user, *args, **kwargs):
        new_room = super().save(commit=False)
        new_room.host = user
        new_room.save()
        return new_room
