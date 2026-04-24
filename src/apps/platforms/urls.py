from django.urls import path

from apps.platforms.views import PlatformListView

urlpatterns = [
    path("", PlatformListView.as_view(), name="platforms-list"),
]
