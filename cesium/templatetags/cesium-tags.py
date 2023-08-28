import os
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=False)
def get_icon(icon_name, icon_class, icon_id):
    path = os.path.join('static', 'icons', icon_name)
    with open(path, 'r') as f:
        svg = f.read().replace('<svg', f'<svg class="{icon_class}" id="{icon_id}"')

    return mark_safe(svg)
