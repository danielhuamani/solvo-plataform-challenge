from apps.notifications.events import UserRegisteredEvent
from apps.notifications.tasks import (
    user_registered_email,
    user_registered_log,
    user_registered_sms,
)


def notify_user_registered(
    *, platform_slug: str, platform_user_id: int, email: str
) -> None:
    event = UserRegisteredEvent(
        platform_slug=platform_slug,
        platform_user_id=platform_user_id,
        email=email,
    )

    user_registered_log.delay(
        platform_slug=event.platform_slug,
        platform_user_id=event.platform_user_id,
        email=event.email,
    )
    user_registered_email.delay(
        platform_slug=event.platform_slug,
        platform_user_id=event.platform_user_id,
        email=event.email,
    )
    user_registered_sms.delay(
        platform_slug=event.platform_slug,
        platform_user_id=event.platform_user_id,
        email=event.email,
    )
