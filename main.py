import asyncio
from fastapi import FastAPI, Body
import uvicorn
from app import *

app = FastAPI()


#        file_bytes = str(data["file"])


@app.get("/api/")
async def default_endpoint():
    return "Hello, i'm python web app"


@app.post("/api/check_title")
async def check_title(data=Body()):
    """Проверка наименования"""
    try:
        input_title = str(data["title"])
        return check_title_function(input_title)
    except Exception as ex:
        print(ex)


@app.post("/api/check_contract_enforced")
async def check_contract_enforced(data=Body()):
    """Проверка обеспечения исполнения контракта"""
    try:
        contract_enforced = str(data["contractEnforced"])
        return check_contract_enforced_function(contract_enforced)
    except Exception as ex:
        print(ex)


@app.post("/api/check_photo")
async def check_photo(data=Body()):
    """Проверка фото"""
    try:
        photo_url = str(data["specifications"])
        return check_photo_function(photo_url)
    except Exception as ex:
        print(ex)

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
