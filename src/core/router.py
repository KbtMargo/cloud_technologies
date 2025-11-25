import datetime
import logging

import sentry_sdk
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/common", tags=["Common"])

logger = logging.getLogger(__name__)


@router.get("/healthcheck")
async def health_check():
    logger.info("[COMMON] Health check called")
    return {"status": "ok", "service": "Library API"}


@router.get("/time")
async def get_time():
    try:
        now = datetime.datetime.now().isoformat()
        return {"server_time": now}
    except Exception as e:
        logger.error(f"Error getting time: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/sentry-debug")
async def trigger_error():
    try:
        division_by_zero = 1 / 0
        return {"division_by_zero": division_by_zero}
    except Exception as e:
        logger.exception("Triggered Sentry error")
        sentry_sdk.capture_exception(e)
        raise HTTPException(status_code=500, detail="Sentry error triggered")
