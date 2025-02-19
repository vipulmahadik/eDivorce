"""
    Mapping between steps in the pre-qualification stage and the questions on each
    step. Useful for showing a human readable link and message when a question is not
    answered. The user can click the link to take them back to the step containing the
    unanswered question.
"""
pre_qual_step_question_mapping = {
    '01': {
        'married_marriage_like'
    },
    '02': {
        'lived_in_bc',
        'lived_in_bc_at_least_year'
    },
    '03': {
        'separation_date',
        'try_reconcile_after_separated',
        'reconciliation_period'
    },
    '04': {
        'children_of_marriage',
        'number_children_under_19',
        'number_children_over_19',
        'children_financial_support'
    },
    '05': {
        'original_marriage_certificate',
        'provide_certificate_later',
        'marriage_certificate_in_english'
    },
    '06': {
        'divorce_reason',
    }
}

"""
    Mapping between questions and steps
    Usage: For each step title, list all questions_keys belong to that step
"""
question_step_mapping = {
    'prequalification': ['married_marriage_like', 'lived_in_bc',
                         'lived_in_bc_at_least_year', 'separation_date',
                         'children_of_marriage',
                         'number_children_under_19',
                         'number_children_over_19',
                         'children_financial_support',
                         'original_marriage_certificate',
                         'provide_certificate_later',
                         'provide_certificate_later_reason',
                         'not_provide_certificate_reason', 'divorce_reason',
                         'marriage_certificate_in_english',
                         'try_reconcile_after_separated',
                         'reconciliation_period'],
    'which_orders': ['want_which_orders'],
    'your_information': ['name_you', 'any_other_name_you', 'other_name_you',
                         'last_name_born_you', 'last_name_before_married_you',
                         'birthday_you', 'lived_in_bc_you',
                         'moved_to_bc_date_you', 'occupation_you'],
    'your_spouse': ['name_spouse', 'any_other_name_spouse', 'other_name_spouse',
                    'last_name_born_spouse', 'last_name_before_married_spouse',
                    'birthday_spouse', 'lived_in_bc_spouse',
                    'moved_to_bc_date_spouse', 'occupation_spouse'],
    'your_marriage': ['when_were_you_married', 'where_were_you_married_city',
                      'where_were_you_married_prov',
                      'where_were_you_married_country',
                      'where_were_you_married_other_country',
                      'marital_status_before_you',
                      'marital_status_before_spouse',
                      'when_were_you_live_married_like'],
    'your_separation': ['no_reconciliation_possible', 'no_collusion'],
    'your_children': ['claimant_children',
                      'how_will_calculate_income',
                      'annual_gross_income',
                      'spouse_annual_gross_income',
                      'payor_monthly_child_support_amount',
                      'special_extraordinary_expenses',
                      'child_support_payor',
                      'claiming_undue_hardship',
                      'claimants_agree_to_child_support_amount',
                      'medical_coverage_available',
                      'whose_plan_is_coverage_under',
                      'child_support_payments_in_arrears',
                      'child_support_arrears_amount',
                      'child_support_in_order',
                      'order_monthly_child_support_amount',
                      'child_support_in_order_reason',
                      'child_support_payment_special_provisions',
                      'number_children_seeking_support',
                      'child_support_amount_under_high_income',
                      'percent_income_over_high_income_limit',
                      'amount_income_over_high_income_limit',
                      'total_guideline_amount',
                      'agree_to_child_support_amount',
                      'agreed_child_support_amount',
                      'reason_child_support_amount',
                      'have_separation_agreement',
                      'have_court_order',
                      'what_parenting_arrangements',
                      'want_parenting_arrangements',
                      'order_respecting_arrangement',
                      'order_for_child_support',
                      'child_support_act',
                      'spouse_number_children_seeking_support',
                      'spouse_child_support_amount_under_high_income',
                      'spouse_percent_income_over_high_income_limit',
                      'spouse_amount_income_over_high_income_limit',
                      'spouse_total_guideline_amount',
                      'spouse_agree_to_child_support_amount',
                      'spouse_agreed_child_support_amount',
                      'spouse_reason_child_support_amount',
                      'you_spouse_entered_agreement',
                      'claimant_debts',
                      'claimant_expenses',
                      'supporting_non_dependents',
                      'supporting_dependents',
                      'supporting_disabled',
                      'undue_hardship',
                      'income_others',
                      'total_income_others',
                      'number_of_children',
                      'time_spent_with_you',
                      'time_spent_with_spouse',
                      'annual_gross_income',
                      'spouse_annual_gross_income',
                      'your_child_support_paid_b',
                      'your_spouse_child_support_paid_b',
                      'your_child_support_paid_c',
                      'your_spouse_child_support_paid_c',
                      'extra_ordinary_expenses_you',
                      'extra_ordinary_expenses_spouse',
                      'additional_relevant_spouse_children_info',
                      'difference_between_claimants',
                      'child_care_expenses',
                      'children_healthcare_premiums',
                      'health_related_expenses',
                      'extraordinary_educational_expenses',
                      'post_secondary_expenses',
                      'extraordinary_extracurricular_expenses',
                      'total_section_seven_expenses',
                      'your_proportionate_share_percent',
                      'your_proportionate_share_amount',
                      'spouse_proportionate_share_percent',
                      'spouse_proportionate_share_amount',
                      'describe_order_special_extra_expenses'
                      ],
    'spousal_support': ['spouse_support_details', 'spouse_support_act'],
    'property_and_debt': ['deal_with_property_debt',
                          'how_to_divide_property_debt',
                          'other_property_claims'],
    'other_orders': ['name_change_you', 'name_change_you_fullname',
                     'name_change_spouse', 'name_change_spouse_fullname',
                     'other_orders_detail'],
    'other_questions': ['address_to_send_official_document_street_you',
                        'address_to_send_official_document_city_you',
                        'address_to_send_official_document_prov_you',
                        'address_to_send_official_document_country_you',
                        'address_to_send_official_document_other_country_you',
                        'address_to_send_official_document_postal_code_you',
                        'address_to_send_official_document_fax_you',
                        'address_to_send_official_document_email_you',
                        'address_to_send_official_document_street_spouse',
                        'address_to_send_official_document_city_spouse',
                        'address_to_send_official_document_prov_spouse',
                        'address_to_send_official_document_country_spouse',
                        'address_to_send_official_document_other_country_spouse',
                        'address_to_send_official_document_postal_code_spouse',
                        'address_to_send_official_document_fax_spouse',
                        'address_to_send_official_document_email_spouse',
                        'divorce_take_effect_on',
                        'divorce_take_effect_on_specific_date'],
    'filing_locations': ['court_registry_for_filing'],
}


""" List of court registries """
list_of_registries = ['Fort St. John', 'Dawson Creek', 'Prince Rupert',
                      'Terrace', 'Smithers', 'Prince George', 'Quesnel',
                      'Williams Lake', 'Campbell River', 'Powell River',
                      'Courtenay', 'Port Alberni', 'Duncan', 'Nanaimo',
                      'Victoria', 'Golden', 'Kamloops', 'Salmon Arm', 'Vernon',
                      'Kelowna', 'Penticton', 'Nelson', 'Rossland', 'Cranbrook',
                      'Chilliwack', 'New Westminster', 'Vancouver',
                      'Fort Nelson', 'Revelstoke']
