"""HTTPS helpers shared by the domain-research scripts. Standard library only."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from functools import lru_cache
from typing import Any, Dict, Optional, Tuple

USER_AGENT = "domain-research-skill/2"


class HttpError(Exception):
    """A failed request. `status` is the HTTP code, or None when nothing came back."""

    def __init__(self, message: str, status: Optional[int] = None, body: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body = body


@lru_cache(maxsize=1)
def ssl_context() -> ssl.SSLContext:
    """The system trust store, or certifi's bundle when Python has no store at all.

    python.org's macOS builds ship without CA certificates until someone runs
    "Install Certificates.command", so every HTTPS call fails verification.
    Falling back only in that case keeps a corporate root in the system store working.
    """
    paths = ssl.get_default_verify_paths()
    if paths.cafile is None and paths.capath is None:
        try:
            import certifi  # type: ignore[import-not-found]
        except ImportError:
            pass
        else:
            return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def _network_error(reason: object, host: str) -> str:
    if isinstance(reason, ssl.SSLCertVerificationError):
        return (
            f"TLS certificate check failed for {host}. This Python has no CA certificates: "
            "run 'Install Certificates.command' from its /Applications/Python 3.x folder, "
            "`pip install certifi`, or use another python3 (Homebrew, /usr/bin/python3)."
        )
    return f"Network error reaching {host}: {reason}"


def _open(req: urllib.request.Request, timeout: float) -> Tuple[int, bytes]:
    host = urllib.parse.urlsplit(req.full_url).hostname or req.full_url
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode(errors="replace")
        raise HttpError(f"HTTP {exc.code} from {host}: {body[:500]}", exc.code, body) from exc
    except urllib.error.URLError as exc:
        raise HttpError(_network_error(exc.reason, host)) from exc
    except OSError as exc:  # timeouts and resets raised outside URLError
        raise HttpError(_network_error(exc, host)) from exc


def request_json(
    url: str,
    *,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Any = None,
    timeout: float = 20.0,
) -> Any:
    """Send a request and decode the JSON response; raises HttpError."""
    data = None if body is None else json.dumps(body).encode()
    all_headers = {"User-Agent": USER_AGENT, "Accept": "application/json", **(headers or {})}
    if data is not None:
        all_headers["Content-Type"] = "application/json"
    _, raw = _open(urllib.request.Request(url, data=data, method=method, headers=all_headers), timeout)
    try:
        return json.loads(raw)
    except ValueError as exc:
        # The host only: a query string can carry an API key.
        host = urllib.parse.urlsplit(url).hostname
        raise HttpError(f"Expected JSON from {host}, got: {raw[:200]!r}") from exc


def status_of(url: str, *, accept: str = "application/json", timeout: float = 20.0) -> Optional[int]:
    """HTTP status of a GET, following redirects; None when the server can't be reached."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    try:
        return _open(req, timeout)[0]
    except HttpError as exc:
        return exc.status
