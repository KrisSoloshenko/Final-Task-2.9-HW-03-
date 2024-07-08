from django import template

register = template.Library()

censor_list = ['года', 'сочи', 'россии']


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
