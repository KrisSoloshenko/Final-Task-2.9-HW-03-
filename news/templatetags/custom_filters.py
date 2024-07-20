from django import template

register = template.Library()

censor_list = ['года']


@register.filter()
def censor(value):
    try:
        if type(value) is str:
            for word in censor_list:
                if word in value.lower().split():
                    value = value.replace(word[1:], "*" * len(word[1:]))
            return value
    except TypeError as e:
        print(e)


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()
