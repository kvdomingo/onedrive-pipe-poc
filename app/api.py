from datetime import datetime
from typing import Any, Coroutine, cast

from fastapi import BackgroundTasks, FastAPI, Request, Response, Security, status
from fastapi.responses import PlainTextResponse
from hamilton import async_driver
from hamilton.async_driver import AsyncDriver
from loguru import logger

from app import etl as _etl
from app.auth import require_bearer

app = FastAPI(
    title="OneDrive Pipe POC",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


async def etl(file_bytes: bytes):
    dr = await cast(
        Coroutine[Any, Any, AsyncDriver],
        async_driver.Builder().with_modules(_etl).build(),
    )
    await dr.execute(
        ["parquet"],
        inputs={"data_bytes": file_bytes},
    )


@app.post("/webhook", dependencies=[Security(require_bearer)])
async def webhook(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
):
    now = datetime.now().isoformat()
    logger.info(f"Webhook received {now}")

    file_bytes = await request.body()
    logger.info(f"Received {len(file_bytes):,} bytes")

    background_tasks.add_task(etl, file_bytes)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
