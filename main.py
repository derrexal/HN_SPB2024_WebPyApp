import asyncio
from typing import Annotated
from fastapi import FastAPI, File
import uvicorn
from checks import check_if_text_in_docx, check_item_quantity, check_item_characteristics, check_delivery_dates

# from transformers import pipeline
import requests
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
async def default_endpoint():
    return "Hello, i'm python web app"

# worked
@app.post("/api/check_title")
async def check_title(file: Annotated[bytes, File()], id: str):
    """Проверка наименования"""
    try:
        response = requests.get(
            f"http://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)
        input_title = str(data["name"])
        return check_if_text_in_docx(input_title, file)
    except Exception as ex:
        print(ex)


# worked
@app.post("/api/check_quantity")
async def check_quantity(file: Annotated[bytes, File()], id: str):
    """
    Проверка того, что количество товаров в КС
    соответствует количеству в ТЗ
    """
    try:
        response = requests.get(
            f"http://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)
        product_items = data['items']
        return check_item_quantity(product_items, file)
    except Exception as ex:
        print(ex)


# worked
@app.post("/api/check_characteristic")
async def check_characteristic(file: Annotated[bytes, File()], id: str):
    """
    Проверка того, что количество характеристик в КС
    соответствует количеству в ТЗ
    """
    try:
        product_items = []

        response_auction_item = requests.get(f"http://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}")
        data_auction_item = json.loads(response_auction_item.text)
        items = data_auction_item['items']
        for item in items:
            response_additional_info = requests.get(f"http://zakupki.mos.ru/newapi/api/Auction/GetAuctionItemAdditionalInfo?itemId={item['id']}")
            data_additional_info = json.loads(response_additional_info.text)
            product_items.append({'product_name': item['name'], 'properties': data_additional_info['characteristics']})

        return check_item_characteristics(product_items, file)
    except Exception as ex:
        print(ex)


@app.post("/api/check_delivery_dates")
async def check_delivery(file: Annotated[bytes, File()], id: str):
    """
    Проверка того, что количество товаров в КС
    соответствует количеству в ТЗ
    """
    try:
        response = requests.get(
            f"http://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)
        product_items = data['deliveries']
        return check_delivery_dates(product_items, file)
    except Exception as ex:
        print(ex)

# если запустить на ноуте сони и немного допилить - будет работать
@app.post("/api/check_photo")
async def check_photo(file: Annotated[bytes, File()], id: str):
    """Проверка фото"""
    try:
        response = requests.get(
            f"http://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)

        image_id = str(data["imageId"]) #TODO: доделать адрес, Артем знает какой. Это только айдишник(Формат урла одинаковый - нужно только вставить image_id)
        # return check_photo_function(photo_url) # TODO: тут использовать функцию Сони - она знает какую. (сейчас закоменченый модуль)
    except Exception as ex:
        print(ex)


async def run():
    config = uvicorn.Config(
        "main:app", host="127.0.0.1", port=5300, log_level="info", loop="none"
    )
    server = uvicorn.Server(config)
    await server.serve()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    loop.close()


if __name__ == "__main__":
    main()
