import time

def default_function_first():
    """Return default plain-text"""
    return "Hello, i'm python web app"


def check_title_function(title: str, file_bytes: str):
    """Проверка наименования"""
    print(f"title: {title}")
    print(f"file_bytes: {file_bytes}")
    time.sleep(4.5)
    return {100, "Проверка наименования выполнена успешно"}


def check_contract_enforced_function(contract_enforced: str, file_bytes: str):
    """Проверка обеспечения исполнения контракта"""
    print(f"contract_enforced: {contract_enforced}")
    print(f"file_bytes: {file_bytes}")
    time.sleep(4.5)
    return {100, "Проверка обеспечения исполнения контракта выполнена успешно"}


def check_photo_function(photo_url: str, file_bytes: str):
    """Проверка фото"""
    print(f"photo_url: {photo_url}")
    print(f"file_bytes: {file_bytes}")
    time.sleep(4.5)
    return {100, "Проверка фото выполнена успешно"}
