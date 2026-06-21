"""Small reusable helpers."""
import re

from .config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Turn arbitrary text into a url-safe slug."""
    return _SLUG_RE.sub("-", text.strip().lower()).strip("-")


def clamp_page_size(requested: int | None) -> int:
    """Clamp a requested page size into the allowed range."""
    if requested is None:
        return DEFAULT_PAGE_SIZE
    return max(1, min(requested, MAX_PAGE_SIZE))


def page_bounds(page: int, page_size: int) -> tuple[int, int]:
    """Return the (offset, limit) for a 1-based page number and size."""
    return (page - 1) * page_size, page_size


def mask_email(email: str) -> str:
    """Mask the local part of an email for logging, e.g. j***@example.com."""
    local, _, domain = email.partition("@")
    if not domain:
        return "***"
    visible = local[0] if local else ""
    return f"{visible}***@{domain}"
