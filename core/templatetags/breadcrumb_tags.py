from django import template
from core.breadcrumbs import BREADCRUMB_MAP, auto_breadcrumb
from django.urls import reverse_lazy

register = template.Library()

@register.simple_tag(takes_context=True)
def get_breadcrumbs(context):
    request = context['request']
    view_name = request.resolver_match.view_name

    breadcrumb_config = BREADCRUMB_MAP.get(view_name)

    if callable(breadcrumb_config):
        breadcrumbs = breadcrumb_config(request, context)
    elif breadcrumb_config:
        breadcrumbs = breadcrumb_config
    else:
        breadcrumbs = auto_breadcrumb(view_name)

    breadcrumbs = [
        crumb for crumb in breadcrumbs
        if isinstance(crumb, dict) and 'label' in crumb and 'url' in crumb
    ]

    home_crumb = {'label': 'Home', 'url': reverse_lazy('core:home')}
    if not breadcrumbs or breadcrumbs[0]['label'] != 'Home':
        breadcrumbs.insert(0, home_crumb)

    return breadcrumbs
