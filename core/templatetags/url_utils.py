from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_current_url(context, url):
    request = context.get('request')
    if request:
        return request.path == url
    return False
