from django import template


register = template.Library()


@register.filter()
def censor(value):
    cens = value
    return cens.replace("t","*")

#символ t - нежелательный