from django import template
import pymorphy3

register = template.Library()
morph = pymorphy3.MorphAnalyzer()


@register.filter
def inflect(value, case='gent'):
    words = value.split()
    declined_words = []

    for word in words:
        parsed = morph.parse(word)[0]
        declined = parsed.inflect({case})

        if declined:
            declined_words.append(declined.word.capitalize())
        else:
            declined_words.append(word)

    return ' '.join(declined_words)
