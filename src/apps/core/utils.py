from django.utils import timezone


def now_local():
    return timezone.localtime(timezone.now())
