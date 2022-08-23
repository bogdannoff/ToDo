from django import template
from mainapp.models import *


register = template.Library()


@register.simple_tag(name='tag_projects')
def get_projects():
    return Projects.objects.all()


@register.simple_tag(name='tag_is_equals')
def is_equals(request, obj):
    return (str(request)==str(obj))


@register.inclusion_tag(name='tag_get_menu', filename='mainapp/left_menu.html')
def get_menu():
    context = {
        'menulist': [
            {'name': 'All', 'url_name': 'tasks'},
            {'name': 'Today', 'url_name': 'today'},
        ],
    }
    return context
