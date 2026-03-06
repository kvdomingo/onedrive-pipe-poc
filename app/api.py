from datetime import datetime

from aiofiles import open
from fastapi import FastAPI, Request, Response, Security, status
from fastapi.responses import PlainTextResponse
from loguru import logger

from app.auth import require_bearer
from app.settings import settings

app = FastAPI(
    title="OneDrive Pipe POC",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/health", response_class=PlainTextResponse)
async def health():
    return "ok"


@app.post("/webhook", dependencies=[Security(require_bearer)])
async def webhook(request: Request, response: Response):
    now = datetime.now().isoformat()
    logger.info(f"Webhook received {now}")

    file_bytes = await request.body()
    logger.info(f"Received {len(file_bytes):,} bytes")

    async with open(
        settings.BASE_DIR / "app/uploads" / f"{now.replace(':', '-')}.xlsx", "wb"
    ) as f:
        await f.write(file_bytes)

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
