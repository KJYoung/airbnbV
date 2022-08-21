from django.contrib import admin
from . import models


class ItemAdmin(admin.ModelAdmin):
    """Item admin definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.RoomType)
class RoomTypeAdmin(ItemAdmin):
    """Room Type admin definition"""

    pass


@admin.register(models.Amenity)
class AmenityAdmin(ItemAdmin):
    """Amenity admin definition"""

    pass


@admin.register(models.Facility)
class FacilityAdmin(ItemAdmin):
    """Facility admin definition"""

    pass


@admin.register(models.HouseRule)
class HouseRuleAdmin(ItemAdmin):
    """House Rule admin definition"""

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo admin definition"""

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """Room admin definition"""

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "name",
                    "host",
                    "description",
                    "country",
                    "city",
                    "room_type",
                    "address",
                    "price",
                )
            },
        ),
        ("Timing", {"fields": ("check_in", "check_out", "instant_book")}),
        (
            "Spaces",
            {
                # "classes": ("collapse",),
                "fields": (
                    "guests",
                    "beds",
                    "bedrooms",
                    "baths",
                    "amenities",
                    "facilities",
                    "house_rules",
                ),
            },
        ),
    )
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
    )

    ordering = ("price", "name")

    list_filter = (
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "instant_book",
        "city",
        "country",
    )

    search_fields = ("=city", "^host__username")

    filter_horizontal = ["amenities", "facilities", "house_rules"]

    def count_amenities(self, obj):
        # return len(obj.amenities.all())
        return obj.amenities.count()

    count_amenities.short_description = "#amenities"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "#photos"
