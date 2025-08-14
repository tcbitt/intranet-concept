from django import template
from core.breadcrumbs import BREADCRUMB_MAP
from django.urls import reverse_lazy

register = template.Library()

@register.simple_tag(takes_context=True)
def get_breadcrumbs(context):
    request = context['request']
    view_name = request.resolver_match.view_name

    breadcrumb_config = BREADCRUMB_MAP.get(view_name)

    if callable(breadcrumb_config):
        breadcrumbs = breadcrumb_config(request, context)
    else:
        breadcrumbs = breadcrumb_config or []

    # Always prepend Home
    home_crumb = {'label': 'Home', 'url': reverse_lazy('core:home')}
    if breadcrumbs and breadcrumbs[0]['label'] != 'Home':
        breadcrumbs.insert(0, home_crumb)

    return breadcrumbs
