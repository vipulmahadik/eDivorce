import json

from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag(takes_context=True)
def input_field(context, type, name='', value='', multiple='', **kwargs):
    """
    Usage:  when specifying data attributes in templates, use "data_" intead of "data-".
    """
    if type == "textarea":
        attributes = additional_attributes(**kwargs)
        if value == '':
            value = context.get(name, '')
        tag = format_html(
            '<textarea name="{}"{}>{}</textarea>',
            name,
            attributes,
            value)
    else:
        # set initial value for textbox
        if type == "text" and value == '' and multiple != 'true':
            value = context.get(name, '')

        attributes = additional_attributes(**kwargs)

        # check if buttons should be selected by default
        checked = ''
        if type == 'checkbox':
            value_list = json.loads(context.get(name, '[]'))
        else:
            value_list = context.get(name, '')

        if value_list is not None and value != '' and value in value_list:
            checked = 'checked'

        tag = format_html(
            '<input type="{}" name="{}" value="{}"{} {}/>',
            type,
            name,
            value,
            attributes,
            checked)

    return tag


def additional_attributes(**kwargs):
    attributes = ''
    for key, data_val in kwargs.items():
        if str.startswith(key, 'data_'):
            key = str.replace(key, 'data_', 'data-')
        attributes = format_html(
            '{} {}="{}"',
            attributes,
            key,
            data_val)
    return attributes


@register.simple_tag
def check_list(source, value):
    """
    Check if given value is in the given source
    """
    try:
        return value in json.loads(source)
    except:
        return False


@register.simple_tag
def multiple_values_to_list(source):
    try:
        return json.loads(source)
    except:
        return []
