import asyncio
from fastapi import FastAPI, Body
import uvicorn
from app import *

app = FastAPI()


@app.get("/api/")
async def default_endpoint():
    """Этот эндпоинт просто возвращает текст по запросу"""
    return default_function_first()


@app.post("/api/check_title")
async def check_title(data=Body()):
    """Проверка наименования"""
    input_title = data["title"]
    file_bytes = str(data["file"])
    return check_title_function(input_title, file_bytes)


@app.post("/api/check_contract_enforced")
async def check_contract_enforced(data=Body()):
    """Проверка обеспечения исполнения контракта"""
    contract_enforced = data["contract_enforced"]
    file_bytes = str(data["file_bytes"])
    return check_contract_enforced_function(contract_enforced, file_bytes)


@app.post("/api/check_photo")
async def check_photo(data=Body()):
    """Проверка фото"""
    photo_url = data["photo_url"]
    file_bytes = str(data["file"])
    return check_photo_function(photo_url, file_bytes)


async def run():
    config = uvicorn.Config("main:app", host="127.0.0.1", port=5300, log_level="info", loop="none")
    server = uvicorn.Server(config)
    await server.serve()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run())
    loop.close()


if __name__ == '__main__':
    main()
