from django import template

register = template.Library()


@register.filter(name='smart_truncate')
def smart_truncate(value, length):
    if len(value) > length:
        return value[:length] + ".."
    return value
