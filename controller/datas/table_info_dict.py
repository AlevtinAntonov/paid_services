# Словарь для определения колонок и идентификаторов в зависимости от таблицы

table_info = {
    'contracts': {
        'column_id': 'contract_id',
        'value_id_index': 0,
        'column_map': {
            1: "contract_number",
            2: "contract_date",
            4: "lesson_name",
            5: "team_name",
            6: "remarks",
            7: "signed",
            8: "cancel_date",
            9: "cancel_agreement_signed",
            10: "without_payment"
        }
    },
    'visit_log': {
        'column_id': 'invoice_id',
        'value_id_index': 0,
        'column_map': {
            2: "lessons_fact",
            3: "lessons_illness",
            4: "lessons_quarantine",
            5: "lessons_other_reasons",
            6: "visit_log_remarks",
        }
    },
    'invoices': {
        'column_id': 'invoice_id',
        'value_id_index': 8,
        'column_map': {
            1: "month_name",
            5: "rest_of_money",
            6: "lessons_per_month",
            7: "remarks",
        }
    },
    'payments': {
        'column_id': 'invoice_id',
        'value_id_index': 8,
        'invoice_id_index': 8,
        'column_map': {
            3: "sum_paid",
            4: "payment_date",
        }
    },
    'lessons': {
        'column_id': 'lesson_id',
        'value_id_index': 0,
        'column_map': {
            2: "lesson_name",
            3: "building_id",
            4: "lesson_rate",
            5: "lessons_per_year",
        }
    },
    'teachers': {
        'column_id': 'teacher_id',
        'value_id_index': 0,
        'column_map': {
            1: "last_name",
            2: "first_name",
            3: "patronymic",
            4: "gender_id",
            5: "phone",
            6: "email",
        }
    },
    'teachers_lessons': {
        'column_id': 'teacher_id',
        'value_id_index': 0,
        'column_map': {
            0: "lesson_id",
            1: "teacher_id",
        }
    }
}
