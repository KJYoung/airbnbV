from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def is_in_favs(context, room):
    user = context.request.user
    favList = list_models.List.objects.get_or_none(
        user=user, name="My Favorite Places"
    )  # Also this code only deals with the only one favList.
    return room in favList.rooms.all()
