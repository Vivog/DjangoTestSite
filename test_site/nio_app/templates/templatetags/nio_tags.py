from django import template

from nio_app.models import *

register = template.Library()


@register.simple_tag()
def get_divisions():
    return Divisions.objects.all()
