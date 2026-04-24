from __future__ import annotations

from celery import shared_task

from apps.notifications.channels import EmailChannel, LogChannel, SmsChannel
from apps.notifications.events import UserRegisteredEvent

@shared_task
def user_registered_log(platform_slug: str, platform_user_id: int, email: str) -> None:
    event = UserRegisteredEvent(
        platform_slug=platform_slug,
        platform_user_id=platform_user_id,
        email=email,
    )
    LogChannel().send(event)


@shared_task
def user_registered_email(platform_slug: str, platform_user_id: int, email: str) -> None:
    event = UserRegisteredEvent(
        platform_slug=platform_slug,
        platform_user_id=platform_user_id,
        email=email,
    )
    EmailChannel().send(event)


@shared_task
def user_registered_sms(platform_slug: str, platform_user_id: int, email: str) -> None:
    event = UserRegisteredEvent(
        platform_slug=platform_slug,
        platform_user_id=platform_user_id,
        email=email,
    )
    SmsChannel().send(event)
