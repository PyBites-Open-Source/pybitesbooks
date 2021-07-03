from django import template

register = template.Library()

# https://sashat.me/2017/01/11/list-of-20-simple-distinct-colors/
COLORS = [
    ("#e6194b", "#fff"),
    ("#3cb44b", "#fff"),
    ("#ffe119", "#000"),
    ("#0082c8", "#fff"),
    ("#f58231", "#fff"),
    ("#911eb4", "#fff"),
    ("#46f0f0", "#000"),
    ("#f032e6", "#fff"),
    ("#d2f53c", "#000"),
    ("#fabebe", "#000"),
    ("#008080", "#fff"),
    ("#e6beff", "#000"),
    ("#aa6e28", "#fff"),
    ("#fffac8", "#000"),
    ("#800000", "#fff"),
    ("#aaffc3", "#000"),
    ("#808000", "#fff"),
    ("#ffd8b1", "#000"),
    ("#000080", "#fff"),
    ("#808080", "#000"),
    ("#FFFFFF", "#000"),
    ("#000000", "#fff"),
]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def user2rgb(userid):
    """Generates a random color for user avatar"""
    idx = userid % len(COLORS)
    bg, fg = COLORS[idx]
    return f'background-color: {bg}; color: {fg};'


@register.filter
def unslugify(value):
    return value.replace('-', ' ')
