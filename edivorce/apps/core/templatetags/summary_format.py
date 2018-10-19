from django import template
import json

from django.utils.html import format_html, format_html_join

register = template.Library()


@register.simple_tag
def reformat_value(source, question_key):
    """
    Reformat user response on summary page
    ie) Remove [], make it a bullet point form
    """
    try:
        lst = json.loads(source)
        if len(lst) == 1:
            return lst[0]
        else:
            return process_list(lst, question_key)
    except:
        if question_key == 'spouse_support_details' or question_key == 'other_orders_detail'\
                or question_key == 'provide_certificate_later_reason' or question_key == 'not_provide_certificate_reason':
            text_list = source.split('\n')
            return process_list(text_list, question_key)
        return source


def process_list(lst, question_key):
    if question_key.startswith('other_name_'):
        list_items = format_html_join(
                    '\n',
                    '<li>{} {}</li>',
                    ((alias_type, value) for alias_type, value in lst if value))
    else:
        list_items = format_html_join(
                    '\n',
                    '<li>{0}</li>',
                    ((value, '') for value in lst if value and not value.isspace()))
    tag = format_html(
        '<ul>{}</ul>',
        list_items)

    return tag


@register.simple_tag
def combine_address(source):
    """
        Reformat address to combine them into one cell with multiple line
        Also show/hide optional questions
    """
    tags = ''

    address_you = ""
    fax_you = ""
    email_you = ""
    address_spouse = ""
    fax_spouse = ""
    email_spouse = ""
    is_specific_date = False
    effective_date = ""

    for item in source:
        q_id = item['question_id']
        if "you" in q_id:
            if "email" not in q_id and "fax" not in q_id:
                if q_id == "address_to_send_official_document_country_you":
                    continue
                address_you = format_html('{}{}<br />', address_you, item["value"])
            elif "fax" in q_id:
                fax_you = item["value"]
            elif "email" in q_id:
                email_you = item["value"]
        elif "spouse" in q_id:
            if "email" not in q_id and "fax" not in q_id:
                if q_id == "address_to_send_official_document_country_spouse":
                    continue
                address_spouse = format_html('{}{}<br />', address_spouse, item["value"])
            elif "fax" in q_id:
                fax_spouse = item["value"]
            elif "email" in q_id:
                email_spouse = item["value"]
        elif q_id == "divorce_take_effect_on":
            if item['value'] == "specific date":
                is_specific_date = True
            else:
                effective_date = item['value']
        elif q_id == "divorce_take_effect_on_specific_date" and is_specific_date:
            effective_date = item['value']

    if address_you != "":
        tags = format_table_data(tags, "What is the best address to send you official court documents?", address_you)
    if fax_you != "":
        tags = format_table_data(tags, "Fax", fax_you)
    if email_you != "":
        tags = format_table_data(tags, "Email", email_you)
    if address_spouse != "":
        tags = format_table_data(tags, "What is the best address to send your spouse official court documents?", address_spouse)
    if fax_spouse != "":
        tags = format_table_data(tags, "Fax", fax_spouse)
    if email_spouse != "":
        tags = format_table_data(tags, "Email", email_spouse)
    if effective_date != "":
        tags = format_table_data(tags, "Divorce is to take effect on", effective_date)

    return tags


@register.simple_tag(takes_context=True)
def marriage_tag(context, source):
    """
        Reformat your_marriage step
        Also show/hide optional questions
    """
    show_all = False
    tags = ''

    marriage_location = ""
    married_date = ""
    married_date_q = ""
    common_law_date = ""
    common_law_date_q = ""
    marital_status_you = ""
    marital_status_you_q = ""
    marital_status_spouse = ""
    marital_status_spouse_q = ""

    # get married_marriage_like value to check if legally married or not
    for question in context.get('prequalification', ''):
        if question['question_id'] == 'married_marriage_like' and question['value'] == 'Legally married':
            show_all = True
            break
        elif question['question_id'] == 'married_marriage_like':
            break

    for item in source:
        q_id = item['question_id']
        value = item['value']
        q_name = item['question__name']

        if q_id == 'when_were_you_married':
            married_date_q = q_name
            married_date = value
        elif q_id == 'when_were_you_live_married_like':
            common_law_date_q = q_name
            common_law_date = value
        elif q_id.startswith('where_were_you_married'):
            if value == 'Other':
                continue
            marriage_location = format_html('{}{}<br />', marriage_location, value)
        elif q_id == 'marital_status_before_you':
            marital_status_you_q = q_name
            marital_status_you = value
        elif q_id == 'marital_status_before_spouse':
            marital_status_spouse_q = q_name
            marital_status_spouse = value

    if show_all and married_date != "":
        tags = format_table_data(tags, married_date_q, married_date)
    if common_law_date != "":
        tags = format_table_data(tags, common_law_date_q, common_law_date)
    if show_all and marriage_location != "":
        tags = format_table_data(tags, "Where were you married", marriage_location)
    if marital_status_you != "":
        tags = format_table_data(tags, marital_status_you_q, marital_status_you)
    if marital_status_spouse != "":
        tags = format_table_data(tags, marital_status_spouse_q, marital_status_spouse)

    return tags


@register.simple_tag
def property_tag(source):
    """
        Reformat your_property and debt step
        Also show/hide optional questions
    """
    tags = ''

    division = division_detail = other_detail = None

    for item in source:
        q_id = item['question_id']

        if q_id == 'deal_with_property_debt':
            division = item
        elif q_id == 'how_to_divide_property_debt':
            division_detail = item
        elif q_id == 'other_property_claims':
            other_detail = item

    if division:
        tags = format_table_data(tags, division['question__name'], division['value'])
    if division and division['value'] == "Unequal division" and division_detail:
        tags = format_table_data(tags, division_detail['question__name'], process_list(division_detail['value'].split('\n'), division_detail['question_id']))
    if other_detail and other_detail['value'].strip():
        tags = format_table_data(tags, other_detail['question__name'], process_list(other_detail['value'].split('\n'), other_detail['question_id']))

    return tags


@register.simple_tag
def prequal_tag(source):
    """
        Reformat prequalification step
        Also show/hide optional questions
    """
    tags = ''

    marriage_status = lived_in_bc = live_at_least_year = separation_date = try_reconcile = reconciliation_period = None
    children_of_marriage = any_under_19 = financial_support = certificate = provide_later = None
    provide_later_reason = not_provide_later_reason = in_english = divorce_reason = None

    for item in source:
        q_id = item['question_id']
        if q_id == 'married_marriage_like':
            marriage_status = item
        elif q_id == 'lived_in_bc':
            lived_in_bc = item
        elif q_id == 'lived_in_bc_at_least_year':
            live_at_least_year = item
        elif q_id == 'separation_date':
            separation_date = item
        elif q_id == 'try_reconcile_after_separated':
            try_reconcile = item
        elif q_id == 'reconciliation_period':
            reconciliation_period = item
        elif q_id == 'children_of_marriage':
            children_of_marriage = item
        elif q_id == 'any_under_19':
            any_under_19 = item
        elif q_id == 'children_financial_support':
            financial_support = item
        elif q_id == 'original_marriage_certificate':
            certificate = item
        elif q_id == 'provide_certificate_later':
            provide_later = item
        elif q_id == 'provide_certificate_later_reason':
            provide_later_reason = item
        elif q_id == 'not_provide_certificate_reason':
            not_provide_later_reason = item
        elif q_id == 'marriage_certificate_in_english':
            in_english = item
        elif q_id == 'divorce_reason':
            divorce_reason = item
            if divorce_reason['value'] == 'live separate':
                divorce_reason['value'] = 'Lived apart for one year'

    if marriage_status:
        tags = format_table_data(tags, marriage_status['question__name'], marriage_status['value'])
    if lived_in_bc:
        tags = format_table_data(tags, lived_in_bc['question__name'], lived_in_bc['value'])
    if live_at_least_year:
        tags = format_table_data(tags, live_at_least_year['question__name'], live_at_least_year['value'])
    if separation_date:
        tags = format_table_data(tags, separation_date['question__name'], separation_date['value'])
    if try_reconcile:
        tags = format_table_data(tags, try_reconcile['question__name'], try_reconcile['value'])
    if try_reconcile and try_reconcile['value'] == 'YES' and reconciliation_period:
        tags = format_table_data(tags, reconciliation_period['question__name'], reconciliation_period_reformat(reconciliation_period['value']))
    if children_of_marriage:
        tags = format_table_data(tags, children_of_marriage['question__name'], children_of_marriage['value'])
    if children_of_marriage and children_of_marriage['value'] == 'YES' and any_under_19:
        tags = format_table_data(tags, any_under_19['question__name'], any_under_19['value'])
    if children_of_marriage and children_of_marriage['value'] == 'YES' and any_under_19 and any_under_19['value'] == 'NO' and financial_support:
        tags = format_table_data(tags, financial_support['question__name'], '<br>'.join(json.loads(financial_support['value'])))
    if certificate:
        tags = format_table_data(tags, certificate['question__name'], certificate['value'])
    if certificate and certificate['value'] == 'NO' and provide_later:
        tags = format_table_data(tags, provide_later['question__name'], provide_later['value'])
    if certificate and provide_later and certificate['value'] == 'NO' and provide_later['value'] == 'YES' and provide_later_reason:
        tags = format_table_data(tags, provide_later_reason['question__name'], process_list(provide_later_reason['value'].split('\n'), provide_later_reason['question_id']))
    if certificate and provide_later and certificate['value'] == 'NO' and provide_later['value'] == 'NO' and not_provide_later_reason:
        tags = format_table_data(tags, not_provide_later_reason['question__name'], process_list(not_provide_later_reason['value'].split('\n'), not_provide_later_reason['question_id']))
    if marriage_status and marriage_status['value'] == 'Living together in a marriage like relationship' and in_english:
        tags = format_table_data(tags, in_english['question__name'], in_english['value'])
    if divorce_reason:
        tags = format_table_data(tags, divorce_reason['question__name'], divorce_reason['value'])

    return tags


@register.simple_tag
def personal_info_tag(source):
    """
        Reformat your information and your spouse step
        Also show/hide optional questions
    """
    tags = ''

    name = other_name = other_name_list = last_name_born = last_name_before = None
    birthday = occupation = lived_bc = moved_bc = None

    for item in source:
        q_id = item['question_id']

        if q_id.startswith('name_'):
            name = item
        elif q_id.startswith('any_other_name_'):
            other_name = item
        elif q_id.startswith('other_name_'):
            other_name_list = item
        elif q_id.startswith('last_name_born_'):
            last_name_born = item
        elif q_id.startswith('last_name_before_married_'):
            last_name_before = item
        elif q_id.startswith('birthday_'):
            birthday = item
        elif q_id.startswith('occupation_'):
            occupation = item
        elif q_id.startswith('lived_in_bc_'):
            lived_bc = item
        elif q_id.startswith('moved_to_bc_date_'):
            moved_bc = item

    if name:
        tags = format_table_data(tags, name['question__name'], name['value'])
    if other_name:
        tags = format_table_data(tags, other_name['question__name'], other_name['value'])
    if other_name and other_name['value'] == 'YES' and other_name_list:
        tags = format_table_data(tags, other_name_list['question__name'], process_list(json.loads(other_name_list['value']), other_name_list['question_id']))
    if last_name_born:
        tags = format_table_data(tags, last_name_born['question__name'], last_name_born['value'])
    if last_name_before:
        tags = format_table_data(tags, last_name_before['question__name'], last_name_before['value'])
    if birthday:
        tags = format_table_data(tags, birthday['question__name'], birthday['value'])
    if occupation:
        tags = format_table_data(tags, occupation['question__name'], occupation['value'])
    if lived_bc and moved_bc and lived_bc['value'] == "Moved to B.C. on":
        tags = format_table_data(tags, lived_bc['question__name'], lived_bc['value'] + ' ' + moved_bc['value'])
    if lived_bc and lived_bc['value'] != "Moved to B.C. on" and lived_bc:
        tags = format_table_data(tags, lived_bc['question__name'], lived_bc['value'])

    return tags


def format_table_data(tags, question, response):
    return format_html(
        '{}<tr><td width="75%" style="padding-right: 5%">{}</td><td width="25%">{}</td></tr>',
        tags,
        question,
        response)


def reconciliation_period_reformat(lst):
    """
        Reformat reconciliation period into From [dd/mm/yyyy] to [dd/mm/yyyy] format
    """
    try:
        lst = json.loads(lst)
    except:
        lst = []
    period = ""
    for f_date, t_date in lst:
        period = format_html('{}From {} to {}<br />', period, f_date, t_date)
    return period
