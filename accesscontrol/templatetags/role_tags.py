from django import template
from accesscontrol.utils import user_has_role

register = template.Library()

@register.simple_tag
def has_role(user, role_name):
    return user_has_role(user, role_name)
'''
Usage example for template tags:

{% load role_tags %}
{% if has_role request.user "Admin" %} 
  <a href="{% url 'admin_dashboard' %}">Admin Dashboard</a>
{% endif %}
'''