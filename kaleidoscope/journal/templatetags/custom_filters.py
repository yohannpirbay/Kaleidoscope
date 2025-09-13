from django import template
import re

register = template.Library()

@register.filter(name='strip_tags')
def strip_tags(value):
    value = re.sub(r'<br\s*/?>', '\n', value)  
    value = re.sub(r'</div>|</p>', '\n', value)  
    return re.sub(r'<[^>]*?>', '', value)
