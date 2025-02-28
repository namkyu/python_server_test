import threading

import uvicorn
from fastapi import FastAPI

from resources import fetch_google

app = FastAPI()


@app.get("/google")
async def call_google():
    return await fetch_google()

@app.get("/threads")
async def get_thread_count():
    return {"active_threads": threading.active_count()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
