import asyncio
from fastapi import FastAPI
import uvicorn

from app import default_function_first

app = FastAPI()


@app.get("/api/")
def default_endpoint():
    """Этот эндпоинт просто возвращает текст по запросу"""
    return default_function_first()


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
