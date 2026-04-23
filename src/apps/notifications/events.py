from dataclasses import dataclass


@dataclass(frozen=True)
class UserRegisteredEvent:
    platform_slug: str
    platform_user_id: int
    email: str
