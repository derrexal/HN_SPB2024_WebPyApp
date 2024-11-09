from const import message_ok, should_be_checked, mostly_correct
from fuzzywuzzy import fuzz, process
import pandas as pd

from utils import get_verdict, fuzzy_sim, find_product_name, extract_table, extract_text_from_docx


def check_if_text_in_docx(text: str, file_bytes: list[int], message: str):
    """
    Ищет в тексте `docx_text` поданный текст.
    Возвращает Ok, если совпадение больше или равно 90,
    Mostly correct, если совпадение от 70 до 90
    И Text should be checked, если значение ниже 70.
    
    Проверяется название КС в ТЗ и адрес в ТЗ
    """
    docx_text = extract_text_from_docx(file_bytes)
    score = fuzz.partial_ratio(text.lower(), docx_text)
    if score >= 90:
        return {'plausibility': score, 'message': message}
    elif 90 > score >= 70:
        return {'plausibility': score, 'message': mostly_correct}
    else:
        return {'plausibility': score, 'message': should_be_checked}


def check_if_products_in_docx(items: list[str], file_bytes: str) -> str:
    """Возвращает Ок, если все товары совпали."""
    data = extract_table(file_bytes)
    data['score'] = data['Наименование товара'].apply(lambda x: process.extractOne(x, items)[1])
    data['verdict'] = data['score'].apply(get_verdict)
    if all(data['verdict'] == 'Ok'):
        return message_ok
    elif any(90 > data['verdict'] >= 70):
        return mostly_correct
    else:
        return should_be_checked


def check_if_quantity_in_docx(product_items: list, data: pd.DataFrame):
    """Возвращает Ок, если все характеристики совпали."""
    for pi in product_items:
        item_title = pi['title']
        item_quantity = pi['quantity'].split(' ')[0]
        item_unit_metric = pi['quantity'].split(' ')[1]
        print(pi['quantity'].split(' '))
        
        df_item = find_product_name(item_title, data).reset_index(drop=True)
        quant_correct = df_item.loc[0, 'Кол-во'] == item_quantity
        metric_correct = fuzzy_sim(item_unit_metric.lower(), df_item.loc[0, 'Ед. изм.'].lower()) >= 90
        print('[INFO] Quant correct: ', quant_correct)
        print('[INFO] Metric correct: ', metric_correct)

        if quant_correct:
            return message_ok
        else:
            return should_be_checked
        