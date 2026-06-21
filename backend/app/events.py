"""Builds notification events handed off to the notifier service."""
from .models import UserInDB

WELCOME_TEMPLATE = "Welcome aboard, {name}!"


def build_welcome_event(user: UserInDB) -> dict[str, str]:
    """Build the welcome notification payload for the notifier queue."""
    return {
        "recipient": user.email,
        "message": WELCOME_TEMPLATE.format(name=user.full_name),
    }
