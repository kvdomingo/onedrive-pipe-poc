from typing import cast

import polars as pl
from aiofiles import open
from loguru import logger

from app.settings import settings


async def excel_bytes(data_bytes: bytes) -> bytes:
    async with open(settings.BASE_DIR / "app/uploads/data.xlsx", "wb") as f:
        await f.write(data_bytes)
    return data_bytes


async def parquet(excel_bytes: bytes) -> pl.DataFrame:
    df = cast(
        pl.DataFrame,
        pl.read_excel(
            excel_bytes,
            infer_schema_length=0,
        ),
    )
    df.write_parquet(settings.BASE_DIR / "app/uploads/data.parquet")
    logger.info(f"Saved {len(df):,} rows to data.parquet")
    return df
