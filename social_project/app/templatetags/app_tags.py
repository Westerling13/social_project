from django import template

register = template.Library()


@register.inclusion_tag('layout/base_tag.html', takes_context=True)
def nav(context, template='nav.html'):
    return {'context': context, 'template': template}
