from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def is_active(request, pattern):
    current_url = resolve(request.path_info).url_name
    return 'active' if current_url == pattern else ''
