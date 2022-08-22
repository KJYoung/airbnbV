from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """List admin definition"""

    list_display = ("name", "user", "count_rooms")

    search_fields = ("name", "user")

    filter_horizontal = ("rooms",)
