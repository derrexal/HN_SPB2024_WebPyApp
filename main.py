import asyncio
from typing import Annotated
from fastapi import FastAPI, File, Body
import uvicorn
from app import *
from checks import check_if_text_in_docx, check_item_quantity

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


@app.post("/api/check_title")
async def check_title(file: Annotated[bytes, File()], id: str):
    """Проверка наименования"""
    try:
        response = requests.get(
            f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)
        input_title = str(data["name"])
        return check_if_text_in_docx(input_title, file)
    except Exception as ex:
        print(ex)


@app.post("/api/check_quantity")
async def check_quantity(file: Annotated[bytes, File()], id: str):
    """
    Проверка того, что количество товаров в КС
    соответствует количеству в ТЗ
    """
    try:
        response = requests.get(
            f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)
        product_items = data['items']
        return check_item_quantity(product_items, file)
    except Exception as ex:
        print(ex)


@app.post("/api/check_contract_enforced")
async def check_contract_enforced(file: Annotated[bytes, File()], id: str):
    """Проверка обеспечения исполнения контракта"""
    try:
        response = requests.get(
            f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)

        contract_enforced = str(data["isContractGuaranteeRequired"])
        return check_contract_enforced_function(contract_enforced)
    except Exception as ex:
        print(ex)


@app.post("/api/check_photo")
async def check_photo(file: Annotated[bytes, File()], id: str):
    """Проверка фото"""
    try:
        response = requests.get(
            f"https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={id}"
        )
        data = json.loads(response.text)

        photo_url = str(data["auctionItem"])
        return check_photo_function(photo_url)
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
