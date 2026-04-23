import logging

from apps.notifications.events import UserRegisteredEvent

logger = logging.getLogger(__name__)


def handle_user_registered(event: UserRegisteredEvent) -> None:
    logger.info(
        "user_registered platform=%s platform_user_id=%s email=%s",
        event.platform_slug,
        event.platform_user_id,
        event.email,
    )
