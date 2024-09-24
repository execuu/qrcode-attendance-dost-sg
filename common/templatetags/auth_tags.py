from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def has_group(user, Officers):
    group = Group.objects.get(name=Officers)
    return True if group in user.groups.all() else False
