import sys

from django import template

from .format_utils import date_formatter
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def effective_date(context, *args, **kwargs):
    """ Returns the effective date of the divorce, based on user's answers """

    effective = 'the 31st day after the date of this order'
    if context['responses']['divorce_take_effect_on'] == 'specific date':
        date = context['responses']['divorce_take_effect_on_specific_date']
        if date == '':
            effective = format_html('<span class="form-entry not-complete"></span>')
        else:
            effective = date_formatter(date)
    return effective

