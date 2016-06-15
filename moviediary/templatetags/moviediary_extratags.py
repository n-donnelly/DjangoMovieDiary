from django import template

register = template.Library()

'''Gets the range for a given integer so we can have
 a "clean" for loop in a template

Taken as snippet from
https://djangosnippets.org/snippets/1357/
 
<ul>{% for i in 3|get_range %}
  <li>{{ i }}. Do something</li>
{% endfor %}</ul>
    '''
@register.filter
def as_range(value):
    return range(value)

@register.filter
def divide(value, arg):
    try:
        return int(value)/int(arg)
    except (ValueError, ZeroDivisionError):
        return None