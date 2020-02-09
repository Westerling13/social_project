from django import template

register = template.Library()


@register.inclusion_tag('layout/base_tag.html', takes_context=True)
def nav(context, template='nav.html', page='index'):
    return {'context': context, 'template': template, 'page': page}
