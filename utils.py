from io import BytesIO

from const import message_ok, mostly_correct, should_be_checked
from fuzzywuzzy import fuzz, process
from docx import Document
import pandas as pd
import json


def extract_table(file_bytes: str, table_num: int = 0) -> pd.DataFrame:
    """Return Table from DOCX file format as DataFrame"""
    with open(file_bytes, 'rb') as f:
        doc = Document(f)
    table_count = len(doc.tables)
    if table_num >= table_count:
        raise BaseException('The count of tables is less than `table_num` argument')
    
    else:
        first_table = doc.tables[table_num]
        
        # Extract the table data into a list of lists
        table_data = []
        for row in first_table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text)
            table_data.append(row_data)
        
        # Convert the list of lists into a Pandas DataFrame
        df = pd.DataFrame(table_data)
        
        # Optionally, set the first row as the header
        df.columns = df.iloc[0]
        df = df[1:]
        
        return(df)


def compare_item_names(web_card: json, doc_df: pd.DataFrame) -> list:
    """
    Extract product items from web card and from document data
    And return the list of product items, that are not literally written in Document
    """
    # Extract item names from web card
    items = []
    for spec in web_card['specifications']:
        items.append(spec['title'])

    item_col = [i for i in doc_df.columns if 'Наименование' in i][0]
    doc_items = doc_df[item_col].to_list()
    
    missing_items = []
    for item in items:
        found = False
        for doc_item in doc_items:
            if item in doc_item:
                found = True
                print(f'[INFO] Item {item} PASSED THE CHECK (V)')
                break
        if not found:
            missing_items.append(item)
            print(f'[INFO] Item {item} HAS NOT PASSED THE CHECK (X)')
    return missing_items


def compare_item_quantity(web_card: json, doc_df: pd.DataFrame):
    # Extract item names from web card
    items = []
    for spec in web_card['specifications']:
        items.append(spec['title'])


# def check_if_text_in_docx(title: str, docx_text: str):
#     score = fuzz.partial_ratio(title.lower(), docx_text)
#     if score >= 90:
#         return message_ok, score
#     elif 90 > score >= 70:
#         return mostly_correct, score
#     else:
#         return should_be_checked, score


def find_product_name(product_item: str, data: pd.DataFrame, column: str='Наименование товара', thresh: int=90) -> tuple[str, int]:
    text, score = process.extractOne(product_item, data[column].to_list())
    if score >= thresh:
        df_product = data[data[column] == text]
        return df_product
    else:
        return "None"


def fuzzy_sim(str1: str, str2: str):
    return fuzz.partial_ratio(str1, str2)


def get_verdict(x: int):
    if x >= 90:
        return message_ok
    elif 90 > x >= 70:
        return mostly_correct
    else:
        return should_be_checked


def extract_text_from_docx(docx_file: list[int]):
    doc = Document(BytesIO(bytearray(docx_file)))
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)

    return ' '.join(full_text)