from django import template
from contact.models import Follows, Room
from django.contrib.auth.models import User
from translate import Translator

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


@register.filter(name='last_message')
def last_mess(roomid):
    messages = Room.objects.get(id=roomid).messages.all()
    if messages.exists():
        return list(messages)[-1].content[:10]
    else:
        return ''


@register.filter
def order_by(queryset, arg):
    return queryset.order_by(arg)


@register.filter(name='get_user')
def get_user(username):
    if User.objects.filter(username=username).exists():
        return User.objects.get(username=username)
    else:
        return False


@register.filter(name='translate')
def translate_text(text):
    translator = Translator(from_lang='en', to_lang='uk-UA')
    return translator.translate(text)
