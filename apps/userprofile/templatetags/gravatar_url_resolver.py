from django import template
from django.conf import settings
import urllib, hashlib
 
register = template.Library()

@register.assignment_tag(takes_context=True)


def get_gravatar_url(context, user, size):
    email = user.get_email()

    #laters
    #prefix = "https://" if context['request'].is_secure() else "http://"
    default = "https://kradalby.no/placeatle.jpg"
    hash = hashlib.md5(email.lower()).hexdigest()

    gravatar_url = "https://www.gravatar.com/avatar/" + hash + "?"    
    gravatar_url += urllib.urlencode({'d': default, 's':str(size)})    
    
    print(hash)

    return gravatar_url
