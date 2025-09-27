from app import app
from fasthtml.common import *
from starlette.responses import RedirectResponse
from starlette.requests import Request
import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."],
        log_level="warning"
    )
