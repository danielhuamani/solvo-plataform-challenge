from apps.notifications.events import UserRegisteredEvent
from apps.notifications.handlers import handle_user_registered


def notify_user_registered(*, platform_slug: str, platform_user_id: int, email: str) -> None:
    event = UserRegisteredEvent(
        platform_slug=platform_slug,
        platform_user_id=platform_user_id,
        email=email,
    )
    handle_user_registered(event)
