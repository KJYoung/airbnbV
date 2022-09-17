from django import template

register = template.Library()


@register.filter()
def custom_filter(value):
    print(value)
    return "Hey!!!!"
