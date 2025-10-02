from typing import Optional

# Starlette Request typing hint for users of this utility
try:
    from starlette.requests import Request  # type: ignore
except Exception:  # pragma: no cover
    Request = object  # type: ignore


def _parse_forwarded_header(val: str) -> tuple[Optional[str], Optional[str]]:
    """Parse Forwarded header like: "proto=https;host=example.com".
    Returns (proto, host) if present.
    """
    if not val:
        return None, None
    parts = [p.strip() for p in val.split(";")]
    kv = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            kv[k.strip().lower()] = v.strip().strip('"')
    return kv.get("proto"), kv.get("host")


def get_base_url(request: "Request") -> str:
    """Return a best-effort absolute base URL for the current request.
    Priority:
    1) Explicit BASE_URL/APP_BASE_URL env var if set (use as-is)
    2) VERCEL_URL env var (https://VERCEL_URL)
    3) Forwarded/X-Forwarded headers from the request
    4) request.url.scheme + request.url.netloc
    5) Fallback: http://127.0.0.1:8000
    """
    import os

    # 1) Explicit override
    base_env = os.getenv("BASE_URL") or os.getenv("APP_BASE_URL")
    if base_env:
        # Ensure it includes a scheme
        if base_env.startswith("http://") or base_env.startswith("https://"):
            return base_env.rstrip("/")
        # Default to https for explicit hostnames
        return f"https://{base_env}".rstrip("/")

    # 2) Vercel environment
    vercel_host = os.getenv("VERCEL_URL")
    if vercel_host:
        # VERCEL_URL is typically the hostname without protocol
        return f"https://{vercel_host}".rstrip("/")

    # 3) Proxy headers
    fwd_hdr = request.headers.get("forwarded") if hasattr(request, "headers") else None
    proto_fwd, host_fwd = _parse_forwarded_header(fwd_hdr or "")

    proto = proto_fwd or (request.headers.get("x-forwarded-proto") if hasattr(request, "headers") else None)
    host = host_fwd or (request.headers.get("x-forwarded-host") if hasattr(request, "headers") else None)

    # 4) Request URL and Host header fallback
    if not proto:
        try:
            proto = request.url.scheme  # type: ignore[attr-defined]
        except Exception:
            proto = None
    if not host:
        # Host header or request.url.netloc
        host = request.headers.get("host") if hasattr(request, "headers") else None
        if not host:
            try:
                host = request.url.netloc  # type: ignore[attr-defined]
            except Exception:
                host = None

    if proto and host:
        return f"{proto}://{host}".rstrip("/")

    # 5) Hard fallback based on environment context
    return "http://127.0.0.1:8000"


def absolute_url(request: "Request", path: str) -> str:
    """Build an absolute URL from a path using the detected base URL.
    Accepts absolute or relative path; normalizes to one leading slash.
    """
    base = get_base_url(request)
    if not path:
        return base
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    # Avoid double slashes
    return base.rstrip("/") + path
