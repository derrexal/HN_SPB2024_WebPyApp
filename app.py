#, file_bytes: str


def check_title_function(title: str):
    """Проверка наименования"""
    print(f"title: {title}")
    return {'plausibility': 100, 'message': 'Проверка наименования выполнена успешно'}


def check_contract_enforced_function(contract_enforced: str):
    """Проверка обеспечения исполнения контракта"""
    print(f"contract_enforced: {contract_enforced}")
    return {'plausibility': 100, 'message': 'Проверка обеспечения исполнения контракта выполнена успешно'}


def check_photo_function(photo_url: str):
    """Проверка фото"""
    print(f"photo_url: {photo_url}")
    return {'plausibility': 100, 'message': 'Проверка фото выполнена успешно'}

