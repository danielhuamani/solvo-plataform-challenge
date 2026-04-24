from abc import ABC, abstractmethod
import logging
from typing import Any


logger = logging.getLogger(__name__)


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, event: Any) -> None:
        raise NotImplementedError


class LogChannel:
    def send(self, event: Any) -> None:
        logger.info(
            "notification channel=log event=%s payload=%s",
            type(event).__name__,
            event.__dict__,
        )


class EmailChannel:
    def send(self, event: Any) -> None:
        logger.info(
            "notification channel=email event=%s payload=%s",
            type(event).__name__,
            event.__dict__,
        )


class SmsChannel:
    def send(self, event: Any) -> None:
        logger.info(
            "notification channel=sms event=%s payload=%s",
            type(event).__name__,
            event.__dict__,
        )
