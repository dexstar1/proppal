import asyncio
import os
import uvicorn

if __name__ == "__main__":
    # Allow overriding defaults via env vars
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    reload_flag = os.getenv("APP_RELOAD", "0").lower() in ("1", "true", "yes")

    try:
        # lifespan="off" prevents Starlette/uvicorn lifespan await from raising
        # CancelledError on Ctrl+C during slow startups
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            reload=reload_flag,
            lifespan="off",
            log_level=os.getenv("UVICORN_LOG_LEVEL", "info"),
            # Windows doesn’t support uvloop; leaving loop default
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        # Gracefully ignore shutdown interrupts to avoid noisy tracebacks
        pass
