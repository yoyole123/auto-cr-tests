"""Application configuration and constants."""
import os

# ponytail: env-driven with dev fallbacks; a real deploy injects these.
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_SECONDS = 60 * 60  # 1 hour

PASSWORD_MIN_LENGTH = 8
MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20
