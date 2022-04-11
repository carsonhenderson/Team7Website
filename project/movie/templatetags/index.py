from django import template

register = template.Library()

## Tutorial found at https://stackoverflow.com/questions/31245245/iterate-through-list-passed-by-custom-template-tag

@register.filter
def index(sequence, position):
    return sequence[position]

@register.filter
def getkey(dict):
    for key, value in dict.items():
        return value
@register.filter
def stars(stars):
    if stars == 5:
        return "images/fivestars.jpg"
    elif stars == 4:
        return "images/fourstars.jpg"
    elif stars == 3:
        return "images/threestars.jpg"
    elif stars == 2:
        return "images/twostars.jpg"
    elif stars == 1:
        return "images/onestar.jpg"
