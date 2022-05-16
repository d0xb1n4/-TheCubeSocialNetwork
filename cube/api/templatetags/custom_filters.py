from django import template
import datetime

register = template.Library()


@register.filter
def get_filename(value):
    return value.split('/')[-1]


@register.filter
def edit_data(value):
    if value.day == datetime.datetime.now().date().day:
        return f'сегодня в {value.hour}:{value.minute}'
    else:
        return value
