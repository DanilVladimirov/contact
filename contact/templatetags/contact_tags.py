from django import template
from contact.models import Follows
from django.contrib.auth.models import User


register = template.Library()


@register.filter(name='strip_gd')
def has_group(url):
    new_url = url.strip('&export=download')
    return new_url


@register.filter(name='followed')
def is_followed(curr_id, another_id):
    check_follow = Follows.objects.get(user=User.objects.get(id=curr_id))
    check_follow = check_follow.another_user.filter(id=another_id)
    if check_follow.exists():
        return True
    else:
        return False
