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
    Prefers Forwarded/X-Forwarded-* headers (useful on Vercel/Proxies),
    falls back to request.url.scheme and request.url.netloc.
    """
    # Forwarded header takes precedence if present
    fwd_hdr = request.headers.get("forwarded") if hasattr(request, "headers") else None
    proto_fwd, host_fwd = _parse_forwarded_header(fwd_hdr or "")

    proto = proto_fwd or (request.headers.get("x-forwarded-proto") if hasattr(request, "headers") else None)
    host = host_fwd or (request.headers.get("x-forwarded-host") if hasattr(request, "headers") else None)

    if not proto:
        try:
            proto = request.url.scheme  # type: ignore[attr-defined]
        except Exception:
            proto = "http"
    if not host:
        # Host header or request.url.netloc
        host = request.headers.get("host") if hasattr(request, "headers") else None
        if not host:
            try:
                host = request.url.netloc  # type: ignore[attr-defined]
            except Exception:
                host = "127.0.0.1:8000"

    return f"{proto}://{host}"


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
    return base + path
