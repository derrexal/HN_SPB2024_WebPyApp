from const import message_ok, should_be_checked, mostly_correct
from fuzzywuzzy import fuzz, process

from utils import get_verdict, fuzzy_sim, extract_table, extract_text_from_docx, \
    retrieve_delivery_time, df_to_list_of_string, save_as_doc

from transformers import pipeline


def check_delivery_address(pipe, text: str, docx_text: str, message: str):
    """
    Возвращает Ок, если График поставки в основном совпадает с информацией в ТЗ.
    """
    answer = retrieve_delivery_time(pipe, docx_text)['answer']
    score = fuzzy_sim(text, answer)
    if score >= 90:
        return {'plausibility': score, 'message': message}
    elif 90 > score >= 70:
        return {'plausibility': score, 'message': mostly_correct}
    else:
        return {'plausibility': score, 'message': should_be_checked}


def check_if_text_in_docx(text: str, file_bytes: bytes):
    """
    Ищет в тексте `docx_text` поданный текст.
    Возвращает Ok, если совпадение больше или равно 90,
    Mostly correct, если совпадение от 70 до 90
    И Text should be checked, если значение ниже 70.

    Проверяется название КС в ТЗ и адрес в ТЗ
    """
    docx_text = extract_text_from_docx(file_bytes)
    if docx_text == "":
        docx_text = save_as_doc(file_bytes)
    score = fuzz.partial_ratio(text.lower(), docx_text)

    return {'plausibility': score, 'message': f'Наименование совпадает на {score} %'}


def check_if_products_in_docx(items: list[str], file_bytes: bytes) -> str:
    """Возвращает Ок, если все товары совпали."""
    data = extract_table(file_bytes)
    if data == "":
        return {'message': 'Пожалуйста, загрузите файл формата docx', 'status': 2}  # 2 - плохо
    data['score'] = data['Наименование товара'].apply(lambda x: process.extractOne(x, items)[1])
    data['verdict'] = data['score'].apply(get_verdict)
    if all(data['verdict'] == 'Ok'):
        return message_ok
    elif any(90 > data['verdict'] >= 70):
        return 'Товары совпали'
    else:
        return 'Требуется обратить внимание на характеристики товара'


# Not Using
# def check_if_quantity_in_docx(product_items: list, data: pd.DataFrame):
#     """Возвращает Ок, если все характеристики совпали."""
#     for pi in product_items:
#         item_title = pi['title']
#         item_quantity = pi['quantity'].split(' ')[0]
#         item_unit_metric = pi['quantity'].split(' ')[1]
#         print(pi['quantity'].split(' '))
#
#         df_item = find_product_name(item_title, data).reset_index(drop=True)
#         quant_correct = df_item.loc[0, 'Кол-во'] == item_quantity
#         metric_correct = fuzzy_sim(item_unit_metric.lower(), df_item.loc[0, 'Ед. изм.'].lower()) >= 90
#         print('[INFO] Quant correct: ', quant_correct)
#         print('[INFO] Metric correct: ', metric_correct)
#
#         if quant_correct:
#             return 'Характеристики совпали'
#         else:
#             return 'Требуется обратить внимание на характеристики товара'


def check_item_quantity(product_items: list, file_bytes: bytes):
    """Проверяет """
    docx_table = extract_table(file_bytes, 0)
    if docx_table == "":
        return {'message': 'Пожалуйста, загрузите файл формата docx', 'status': 2} # 2 - плохо
    quant_errors = []
    doc_items = df_to_list_of_string(docx_table)
    for item in product_items:
        item_name = item['name']
        item_quant = str(item['currentValue']) + ' ' + item['okeiName']
        text, score = process.extractOne(item_name, doc_items)
        quant_score = fuzz.partial_ratio(item_quant.lower(), text.lower())
        if quant_score <= 70:
            quant_errors.append((item_name, item_quant))
    #TODO: если нужно можем поделить len(quant_errors) на len(product_items) и получить score
    if len(quant_errors) == 0:
        return {'message': 'Количество товаров спецификации совпадает', 'additional_info': quant_errors}
    else:
        return {'message': 'Требуется обратить внимание на количество товаров в спецификации', 'additional_info': quant_errors}


def check_item_characteristics(product_items: list, file_bytes: bytes):
    docx_table = extract_table(file_bytes, 0)
    if docx_table == "":
        return {'message': 'Пожалуйста, загрузите файл формата docx', 'status': 2}
    char_errors = []
    doc_items = df_to_list_of_string(docx_table)
    for item in product_items:
        item_name = item['product_name']
        item_char = item['properties']
        text, score = process.extractOne(item_name, doc_items)
        item_chars = [{d['name']: d['value']} for d in item_char]
        for item_char in item_chars:
            for ic in item_char:
                char_score = fuzz.partial_ratio(str(ic) + ':', text)
                if char_score < 60:
                    char_errors.append((item_name, ic, item_char[ic]))
    #TODO: если нужно можем поделить len(quant_errors) на len(product_items) и получить score
    if len(char_errors) == 0:
        return {'message': 'Характеристики товаров спецификации совпадают', 'additional_info': char_errors}
    else:
        return {'message': 'Требуется обратить внимание на характеристики товаров в спецификации', 'additional_info': char_errors}


def check_delivery_dates(product_items: list, file_bytes: bytes):
    docx_text = extract_text_from_docx(file_bytes)
    if docx_text == "":
        docx_text = save_as_doc(file_bytes)
    pipe = pipeline("question-answering", model="timpal0l/mdeberta-v3-base-squad2")
    delivery_errors = []

    for item in product_items:
        for i in item["items"]:
            item_name = i['name']
            item_delivery_dates = item['periodDaysTo']
            # TODO: на случай чего оставил упрощенную версию проверки
            tz_delivery_dates = pipe('Какой график/срок поставки в днях?', docx_text)
            # score = fuzz.partial_ratio(item_delivery_dates, tz_delivery_dates)
            delivery_score = fuzz.partial_ratio(str(item_delivery_dates), tz_delivery_dates['answer'])
            if delivery_score < 80:
                delivery_errors.append((item_name, tz_delivery_dates))

    if len(delivery_errors) == 0:
        return {'message': 'График поставки товаров спецификации совпадают', 'additional_info': delivery_errors}
    else:
        return {'message': 'Требуется обратить внимание на график поставки товаров в спецификации', 'additional_info': delivery_errors}